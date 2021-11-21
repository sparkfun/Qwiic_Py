# this file provides the __future__ module for micropython boards

def print_function(*args):
  print(*args)

def division(*args):
  print(*args)
  raise Exception('division is not implemented yet for micropython qwiic. please consider writing an implementation...')
