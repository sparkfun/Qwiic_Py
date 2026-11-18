#!/usr/bin/env python3
"""Build the Doxygen API reference for every driver into one site.

Each driver gets site/<driver>/ (published at docs.sparkfun.com/Qwiic_Py/<driver>/),
built with the shared config in docs/doxygen/Doxyfile. site/index.html lists
every driver.

Usage:
    build_docs.py [--output site] [--strict] [driver ...]

--strict prints Doxygen's warnings and fails if there are any (CI uses it).

Needs doxygen on PATH.
"""

import argparse
import html
import os
import shutil
import subprocess
import sys

from qwiic_repo import REPO_ROOT, load_drivers

DOXYFILE = os.path.join(REPO_ROOT, "docs", "doxygen", "Doxyfile")


def build_driver(driver, output, strict=False):
    out = os.path.join(output, driver.name)
    os.makedirs(out, exist_ok=True)
    inputs = [os.path.join(driver.path, rel) for rel in driver.python_files()]
    inputs.append(os.path.join(driver.path, "README.md"))
    # The README links to examples/README.md; as an input it becomes an
    # Examples page, so those links work on the docs site too
    examples_readme = os.path.join(driver.path, "examples", "README.md")
    if os.path.exists(examples_readme):
        inputs.append(examples_readme)
    images = os.path.join(driver.path, "docs", "images")
    env = dict(os.environ)
    env.update({
        "QWIIC_DOC_ROOT": REPO_ROOT,
        "QWIIC_DOC_NAME": driver.name,
        "QWIIC_DOC_BRIEF": driver.pyproject["project"].get("description", ""),
        "QWIIC_DOC_VERSION": driver.version,
        "QWIIC_DOC_OUTPUT": out,
        "QWIIC_DOC_INPUT": " ".join('"%s"' % p for p in inputs),
        "QWIIC_DOC_EXCLUDE": "",
        "QWIIC_DOC_IMAGES": '"%s"' % images if os.path.isdir(images) else "",
        "QWIIC_DOC_MAINPAGE": os.path.join(driver.path, "README.md"),
    })
    result = subprocess.run(["doxygen", DOXYFILE], cwd=driver.path, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    if result.returncode != 0:
        print(result.stdout)
        raise SystemExit("doxygen failed for " + driver.name)
    warnings = [line for line in result.stdout.splitlines() if "warning:" in line or "error:" in line]
    print("built", os.path.relpath(out))
    if strict:
        for line in warnings:
            print("  " + line.replace(REPO_ROOT + os.sep, ""))
    return len(warnings)


def write_index(drivers, output):
    rows = "\n".join(
        '<tr><td><a href="%s/">%s</a></td><td>%s</td><td>%s</td></tr>'
        % (d.name, d.name, html.escape(d.pyproject["project"].get("description", "")), d.version)
        for d in drivers
    )
    with open(os.path.join(output, "index.html"), "w") as f:
        f.write(
            "<!doctype html><html><head><meta charset='utf-8'><title>SparkFun Qwiic Python API reference</title>"
            "<style>body{font-family:sans-serif;max-width:60em;margin:2em auto;padding:0 1em}"
            "td{padding:.3em 1em .3em 0;vertical-align:top}</style></head><body>"
            "<h1>SparkFun Qwiic Python API reference</h1>"
            "<p>Source and install instructions: <a href='https://github.com/sparkfun/Qwiic_Py'>github.com/sparkfun/Qwiic_Py</a></p>"
            "<table><tr><th>Driver</th><th>Description</th><th>Version</th></tr>%s</table></body></html>" % rows
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", default=os.path.join(REPO_ROOT, "site"))
    parser.add_argument("--strict", action="store_true", help="fail on any Doxygen warning")
    parser.add_argument("drivers", nargs="*")
    args = parser.parse_args()
    if not shutil.which("doxygen"):
        sys.exit("doxygen is not installed")
    output = os.path.abspath(args.output)
    drivers = load_drivers(args.drivers or None)
    warnings = 0
    for driver in drivers:
        warnings += build_driver(driver, output, args.strict)
    write_index(load_drivers(), output)
    if args.strict and warnings:
        sys.exit("%d Doxygen warning(s)" % warnings)


if __name__ == "__main__":
    main()
