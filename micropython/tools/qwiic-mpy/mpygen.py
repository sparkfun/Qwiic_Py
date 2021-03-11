#!/usr/bin/env python
import argparse
import subprocess
import shutil
import json
import glob
import os
from braceexpand import braceexpand 

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

def main ():
  print('')
  if args.clean:
    print('cleaning output dir: ' + args.dest)
    shutil.rmtree(args.dest)
    print('done')
    return

  print('loading config: ' + args.options)
  with open(args.options, 'r') as f:
    cfg = json.load(f)
  print('')
  
  print('generating exclude patterns: ')
  expanded = []
  for pattern in cfg['exclude']:
    expanded.extend(braceexpand(pattern))
  patterns = map(lambda p: os.path.join(args.root, p), expanded)
  exclude = []
  for pattern in patterns:
    exclude.extend(glob.iglob(pattern, recursive=True))
  print('excluding ' + str(len(exclude)) + ' files')
  print('use -v option to see all excluded files')
  for f in exclude:
    verboseprint('\t', f)
  print('')

  def include (p):    # use closure of 'exclude' for simple boolean check if a file can be included
    if p in exclude:
      return False
    return True

  print('generating .mpy files:')
  expanded = []
  for pattern in cfg['patterns']:
    expanded.extend(braceexpand(pattern))
  patterns = map(lambda p: os.path.join(args.root, p), expanded)
  for pattern in patterns:
    print('globbing pattern: ' + pattern)
    included = filter(include, glob.iglob(pattern, recursive=True))     # use 'include' function to filter out excluded files from glob pattern

    for src in included:
      rel = os.path.relpath(src, os.path.commonpath([src, args.root]))  # relative path from root to src file
      dependent = os.path.join(args.dest, rel)                          # dependent filepath (under construction from relative path)
      dep_base, dep_ext = os.path.splitext(dependent)                   # intermediate var to help build dependent filepath
      dependent = dep_base + '.mpy'                                     # dependent file path (think of 'target' file - this is the .mpy file we will generate from the src file)
      enclosing_dir = os.path.dirname(dependent)                        # enclosing dir of dependent file

      if not os.path.exists(enclosing_dir):                             
        os.makedirs(enclosing_dir)                                      # mkdir -p

      regen = True                                                      # assume regeneration is necessary
      if os.path.exists(dependent):                                       # if dependent file exists
        src_mtime = os.path.getmtime(src)
        dependent_mtime = os.path.getmtime(dependent)
        if dependent_mtime >= src_mtime:                                  # and is not older than the src file
          regen = False                                                     # then we do not need to regen

      if regen:                                                         # use the subprocess module to run the mpy-cross cross compiler on the src file to 
        cmd = [args.mpy_cross]                                          # generate the target file according to config settings from the configuration file (loaded at startup)
        cmd.extend(cfg['mpy-cross']['flags'])
        cmd.extend([src])
        cmd.extend(['-o', dependent])

        print(f'\t{bcolors.OKBLUE}regen: {bcolors.ENDC}' + dependent)
        verbose_output = ['\t']
        verbose_output.extend(list(map(lambda s: str(s) + ' ', cmd)))
        verboseprint(*verbose_output)
        
        results = subprocess.run( cmd, capture_output=True)
        stdout = str(results.stdout)
        if stdout != "b''":
          verboseprint(str(stdout))
        stderror = str(results.stderr)
        if stderror != "b''":
          print(f'{bcolors.FAIL}error: {str(results.stderr)}{bcolors.ENDC}')


# ******************************************************************************
#
# Main program flow
#
# ******************************************************************************
if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='generate compiled bytecode for micropython from Qwiic_Py')

  parser.add_argument('-m', '--mpy-cross', dest='mpy_cross', required=True, help='path to mpy-cross executable')
  parser.add_argument('-r', '--root', dest='root', required=False, default='.', help='path to root of Qwiic_Py repo')
  parser.add_argument('-d', '--dest', dest='dest', required=False, default='./micropython/dist', help='path to root folder of output - contents will be overwritten')
  parser.add_argument('-o', '--options', dest='options', required=False, default='./micropython/tools/qwiic-mpy/cfg.json', help='path to configuration json file')
  parser.add_argument('-c', '--clean', required=False, default=0, help='clean the output directory', action='store_true')
  parser.add_argument('-v', '--verbose', required=False, default=0, help='enable verbose output', action='store_true')

  args = parser.parse_args()

  # Create print function for verbose output if caller deems it: https://stackoverflow.com/questions/5980042/how-to-implement-the-verbose-or-v-option-into-a-script
  if args.verbose:
    def verboseprint(*args):
      # Print each argument separately so caller doesn't need to
      # stuff everything to be printed into a single string
      for arg in args:
        print(arg, end='', flush=True)
      print()
  else:
    verboseprint = lambda *a: None      # do-nothing function

  def twopartprint(verbosestr, printstr):
    if args.verbose:
      print(verbosestr, end = '')

    print(printstr)

  main()
