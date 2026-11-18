#!/usr/bin/env python3
"""Bump one package's version and regenerate everything that copies it.

Usage:
    bump_version.py <package> <version | major | minor | patch>

<package> is a driver (qwiic_bme280), qwiic_i2c, or qwiic (the sparkfun-qwiic
meta-package). The version is X.Y.Z, or major/minor/patch to increment the
current one.

Sets the version in the package's pyproject.toml and __version__ in its
modules, then runs gen_package_json.py and gen_registry.py. Those update the
mip manifests (including other drivers' manifests, which pin their
dependencies to release tags), the meta-package's dependency list and
docs/drivers.md.
"""

import argparse
import os
import re
import subprocess
import sys

from qwiic_repo import (
    REPO_ROOT,
    Driver,
    die,
    driver_names,
    load_drivers,
    normalize_dist_name,
    read_text,
    requirement_name,
)

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
META_NAME = "qwiic"
VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
PYPROJECT_VERSION_RE = re.compile(r'^version = "([^"]*)"$', re.MULTILINE)
MODULE_VERSION_RE = re.compile(r'^__version__ = "([^"]*)"$', re.MULTILINE)


def package_files(name):
    """(pyproject.toml path, [module files that carry __version__]) of a package."""
    if name == META_NAME:
        meta = os.path.join(REPO_ROOT, META_NAME)
        return os.path.join(meta, "pyproject.toml"), [os.path.join(meta, "qwiic.py")]
    if name not in driver_names():
        die("%s: no such package (expected a directory in drivers/, qwiic_i2c or qwiic)" % name)
    driver = Driver(name)
    return os.path.join(driver.path, "pyproject.toml"), driver.version_files()


def parse_version(text):
    match = VERSION_RE.match(text)
    if not match:
        die("%r is not a version: use X.Y.Z, major, minor or patch" % text)
    return tuple(int(part) for part in match.groups())


def next_version(current, request):
    major, minor, patch = parse_version(current)
    if request == "major":
        return "%d.0.0" % (major + 1)
    if request == "minor":
        return "%d.%d.0" % (major, minor + 1)
    if request == "patch":
        return "%d.%d.%d" % (major, minor, patch + 1)
    if parse_version(request) <= (major, minor, patch):
        die("%s is not newer than the current version %s" % (request, current))
    return request


def replace_version(path, pattern, version):
    """Replace the one version line pattern matches in path; return the old version."""
    text = read_text(path)
    matches = pattern.findall(text)
    if len(matches) != 1:
        die("%s: expected one version line, found %d" % (os.path.relpath(path), len(matches)))
    new_text = pattern.sub(lambda m: m.group(0).replace(m.group(1), version), text, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return matches[0]


def run_tool(script):
    subprocess.run([sys.executable, os.path.join(TOOLS_DIR, script)], check=True, cwd=REPO_ROOT)


def excluded_dependents(name, version):
    """Drivers whose requirement on name has an upper bound the new version reaches."""
    if name == META_NAME:
        return []
    dist = normalize_dist_name(Driver(name).dist_name)
    major = parse_version(version)[0]
    found = []
    for driver in load_drivers():
        for requirement in driver.dependencies:
            if requirement_name(requirement) != dist:
                continue
            bound = re.search(r"<\s*(\d+)(?:[.,\s;]|$)", requirement)
            if bound and major >= int(bound.group(1)):
                found.append((driver.name, requirement))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("package", help="driver name, qwiic_i2c or qwiic")
    parser.add_argument("version", help="X.Y.Z, major, minor or patch")
    args = parser.parse_args()

    pyproject, modules = package_files(args.package)
    current = PYPROJECT_VERSION_RE.findall(read_text(pyproject))
    if len(current) != 1:
        die("%s: expected one version line, found %d" % (os.path.relpath(pyproject), len(current)))
    version = next_version(current[0], args.version)

    replace_version(pyproject, PYPROJECT_VERSION_RE, version)
    for module in modules:
        replace_version(module, MODULE_VERSION_RE, version)
    # Flush so this comes before the generators' output
    print("%s: %s -> %s" % (args.package, current[0], version), flush=True)

    run_tool("gen_package_json.py")
    run_tool("gen_registry.py")

    for dependent, requirement in excluded_dependents(args.package, version):
        print("warning: %s requires %r, which excludes %s; update and test it" % (dependent, requirement, version))

    print()
    print("Next: open a pull request with these changes. After it merges, tag main and push the tag:")
    print("    git tag %s-%s && git push origin %s-%s" % (args.package, version, args.package, version))
    print("Push the tag straight away: other drivers' mip manifests may already point to it.")


if __name__ == "__main__":
    main()
