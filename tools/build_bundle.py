#!/usr/bin/env python3
"""Build the SparkFun Qwiic CircuitPython bundle for circup.

circuitpython-build-bundles assumes every library is its own git repository
(it reads each library's name from `git remote` and its version from
`git describe`), so it can't build from this monorepo. This script builds the
same layout from each driver's pyproject.toml instead:

    bundles/qwiic-py-<platform>-<tag>.zip     platform = py, 9.x-mpy, 10.x-mpy, ...
        qwiic-py-<platform>-<tag>/
            lib/<module>.py|.mpy, lib/<package>/...
            examples/<driver>/...
            requirements/<library>/requirements.txt, pyproject.toml
            README.txt, VERSIONS.txt
    bundles/qwiic-py-examples-<tag>.zip
    bundles/qwiic-py-<tag>.json

Users add it with `circup bundle-add sparkfun/Qwiic_Py`. circup finds the newest
bundle through the repository's latest GitHub Release, so publish each bundle
as a Release named <tag> with these files attached.

Usage:
    build_bundle.py [--tag YYYYMMDD] [--output bundles] [--py-only]
                    [--mpy-cross NAME=PATH ...]

Without --mpy-cross, .mpy bundles use circuitpython-build-tools to build
CircuitPython's mpy-cross for each supported version (needs a C toolchain).
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

from qwiic_repo import GITHUB_REPO, drivers_by_dist_name, load_drivers, requirement_marker, requirement_name

PREFIX = "qwiic-py"

README = """This is the SparkFun Qwiic CircuitPython bundle, built from
https://github.com/{repo}

Add it to circup once:
    circup bundle-add {repo}
then install drivers by name, for example:
    circup install qwiic_bme280
    circup example qwiic_bme280/qwiic_bme280_ex1_basic_readings
"""


class Library(object):
    """One circup library: a module or package in lib/, plus its metadata."""

    def __init__(self, name, driver, files, requires, is_package):
        self.name = name
        self.driver = driver
        self.files = files            # [(path in lib/, source path)]
        self.requires = requires      # other library names
        self.is_package = is_package


def collect_libraries():
    by_dist = drivers_by_dist_name()
    libraries = []
    for driver in load_drivers():
        if "circuitpython" not in driver.platforms:
            continue
        requires = []
        for requirement in driver.dependencies:
            if requirement_marker(requirement):
                continue
            dep = by_dist.get(requirement_name(requirement))
            if dep is not None:
                requires.append(main_library_name(dep))

        modules = driver.bundle_modules or driver.py_modules
        if modules:
            main, extra = modules[0], modules[1:]
            # Extra modules (qwiic_i2c's platform backend) are their own
            # libraries that the main one requires
            for module in extra:
                libraries.append(Library(module, driver, [(module + ".py", os.path.join(driver.path, module + ".py"))], [], False))
            libraries.append(Library(main, driver, [(main + ".py", os.path.join(driver.path, main + ".py"))], requires + list(extra), False))
        for package in driver.packages:
            files = [(dest, os.path.join(driver.path, src)) for dest, src in driver.source_files() if dest.startswith(package + "/")]
            libraries.append(Library(package, driver, files, requires, True))
    return libraries


def main_library_name(driver):
    modules = driver.bundle_modules or driver.py_modules
    return modules[0] if modules else driver.packages[0]


def compile_mpy(mpy_cross, source, dest):
    result = subprocess.run([mpy_cross, "-o", dest, source], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    if result.returncode != 0:
        raise SystemExit("mpy-cross failed on %s:\n%s" % (source, result.stdout))


def write_tree(root, libraries, drivers, platform, mpy_cross, tag):
    top = os.path.join(root, "%s-%s-%s" % (PREFIX, platform, tag))
    for library in libraries:
        for dest, source in library.files:
            if mpy_cross and dest.endswith(".py"):
                out = os.path.join(top, "lib", dest[:-3] + ".mpy")
                os.makedirs(os.path.dirname(out), exist_ok=True)
                compile_mpy(mpy_cross, source, out)
            else:
                out = os.path.join(top, "lib", dest)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                shutil.copyfile(source, out)
        req_dir = os.path.join(top, "requirements", library.name)
        os.makedirs(req_dir, exist_ok=True)
        with open(os.path.join(req_dir, "requirements.txt"), "w") as f:
            f.write("".join(name + "\n" for name in library.requires))
        shutil.copyfile(os.path.join(library.driver.path, "pyproject.toml"), os.path.join(req_dir, "pyproject.toml"))
    write_examples(top, drivers)
    with open(os.path.join(top, "README.txt"), "w") as f:
        f.write(README.format(repo=GITHUB_REPO))
    with open(os.path.join(top, "VERSIONS.txt"), "w") as f:
        f.write(tag + "\r\n")
        for driver in drivers:
            f.write("https://github.com/%s/releases/tag/%s\r\n" % (GITHUB_REPO, driver.tag))
    return top


def write_examples(top, drivers):
    for driver in drivers:
        examples = os.path.join(driver.path, "examples")
        if not os.path.isdir(examples):
            continue
        out = os.path.join(top, "examples", driver.name)
        os.makedirs(out, exist_ok=True)
        for name in sorted(os.listdir(examples)):
            if name.endswith(".py") or name == "README.md":
                shutil.copyfile(os.path.join(examples, name), os.path.join(out, name))


def zip_tree(top, zip_path):
    base = os.path.dirname(top)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, _, files in os.walk(top):
            for name in sorted(files):
                path = os.path.join(folder, name)
                z.write(path, os.path.relpath(path, base))


def bundle_json(libraries):
    data = {}
    for library in libraries:
        driver = library.driver
        data[library.name] = {
            "package": library.is_package,
            "pypi_name": driver.dist_name if library.name == main_library_name(driver) else "",
            "version": driver.version,
            "repo": "https://github.com/%s/tree/main/drivers/%s" % (GITHUB_REPO, driver.name),
            "path": "lib/" + library.name,
            "dependencies": list(library.requires),
            "external_dependencies": [],
            "pypi_description": driver.pyproject["project"].get("description", ""),
        }
    return data


def mpy_compilers(args, work):
    if args.py_only:
        return []
    if args.mpy_cross:
        compilers = []
        for item in args.mpy_cross:
            name, _, path = item.partition("=")
            compilers.append((name, path))
        return compilers
    try:
        from circuitpython_build_tools import build, target_versions
    except ImportError:
        raise SystemExit("pip install circuitpython-build-tools, or pass --mpy-cross NAME=PATH / --py-only")
    compilers = []
    old = os.getcwd()
    os.chdir(work)  # build.mpy_cross builds into ./build_deps
    try:
        for version in target_versions.VERSIONS:
            compilers.append((version["name"], os.path.abspath(build.mpy_cross(version))))
    finally:
        os.chdir(old)
    return compilers


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", default=datetime.date.today().strftime("%Y%m%d"))
    parser.add_argument("--output", default="bundles")
    parser.add_argument("--py-only", action="store_true", help="only build the .py bundle")
    parser.add_argument("--mpy-cross", action="append", help="NAME=PATH, for example 10.x=/path/to/mpy-cross (repeatable)")
    args = parser.parse_args()

    libraries = collect_libraries()
    drivers = [d for d in load_drivers() if "circuitpython" in d.platforms]
    os.makedirs(args.output, exist_ok=True)

    with tempfile.TemporaryDirectory() as work:
        targets = [("py", None)] + [("%s-mpy" % name, path) for name, path in mpy_compilers(args, work)]
        for platform, mpy_cross in targets:
            top = write_tree(work, libraries, drivers, platform, mpy_cross, args.tag)
            zip_path = os.path.join(args.output, "%s-%s-%s.zip" % (PREFIX, platform, args.tag))
            zip_tree(top, zip_path)
            print("wrote", zip_path)

        examples_top = os.path.join(work, "%s-examples-%s" % (PREFIX, args.tag))
        write_examples(examples_top, drivers)
        zip_path = os.path.join(args.output, "%s-examples-%s.zip" % (PREFIX, args.tag))
        zip_tree(examples_top, zip_path)
        print("wrote", zip_path)

    json_path = os.path.join(args.output, "%s-%s.json" % (PREFIX, args.tag))
    with open(json_path, "w") as f:
        json.dump(bundle_json(libraries), f, indent=2, sort_keys=True)
    print("wrote", json_path)


if __name__ == "__main__":
    sys.exit(main())
