#!/usr/bin/env python3
"""Generate each driver's mip manifests from its pyproject.toml.

Writes drivers/<name>/package.json (the driver) and
drivers/<name>/examples/package.json (its examples). URLs are relative, so mip
resolves them from the manifest's own directory and applies the @tag a user
asks for. Dependencies on other drivers in this repo point at their directory
and are pinned to their release tag.

Usage:
    gen_package_json.py [--check] [driver ...]

--check writes nothing and exits 1 if any manifest is out of date (for CI).
"""

import argparse
import json
import os
import sys

from qwiic_repo import (
    drivers_by_dist_name,
    load_drivers,
    read_text,
    requirement_marker,
    requirement_name,
)


def manifest_text(manifest):
    """JSON with one [destination, source] pair per line, like hand-written manifests."""
    lines = ["{"]
    keys = [k for k in ("urls", "deps") if k in manifest]
    for key in keys:
        lines.append('    "%s": [' % key)
        pairs = [json.dumps(pair) for pair in manifest[key]]
        lines.extend("        %s%s" % (pair, "," if i < len(pairs) - 1 else "") for i, pair in enumerate(pairs))
        lines.append("    ],")
    lines.append('    "version": %s' % json.dumps(manifest["version"]))
    lines.append("}")
    return "\n".join(lines) + "\n"


def driver_manifest(driver, by_dist):
    deps = []
    for requirement in driver.dependencies:
        if requirement_marker(requirement):
            # Platform-specific (for example smbus2 on Linux): not for mip
            continue
        dep = by_dist.get(requirement_name(requirement))
        if dep is None:
            raise SystemExit("%s: dependency %r is not a driver in this repo" % (driver.name, requirement))
        deps.append([dep.mip_path, dep.tag])
    manifest = {
        "urls": [[dest, src] for dest, src in driver.source_files(driver.mip_modules)],
        "version": driver.version,
    }
    if deps:
        manifest["deps"] = deps
    return manifest


def examples_manifest(driver):
    folder = driver.name + "_examples"
    return {
        "urls": [[folder + "/" + name, name] for name in driver.example_files()],
        "version": driver.version,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report out-of-date manifests instead of writing")
    parser.add_argument("drivers", nargs="*")
    args = parser.parse_args()

    by_dist = drivers_by_dist_name()
    stale = []
    for driver in load_drivers(args.drivers or None):
        outputs = {}
        if "micropython" in driver.platforms:
            outputs[os.path.join(driver.path, "package.json")] = manifest_text(driver_manifest(driver, by_dist))
            if driver.example_files():
                outputs[os.path.join(driver.path, "examples", "package.json")] = manifest_text(examples_manifest(driver))
        for path, text in outputs.items():
            current = read_text(path) if os.path.exists(path) else None
            if current == text:
                continue
            if args.check:
                stale.append(os.path.relpath(path))
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
                print("wrote", os.path.relpath(path))

    if stale:
        print("Out of date (run tools/gen_package_json.py):", file=sys.stderr)
        for path in stale:
            print("  " + path, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
