#!/usr/bin/env python3
"""Write the final commit for each old per-driver repository.

Before the old repositories are archived, each gets one last commit that
points users at the driver's new home in Qwiic_Py:

- README.md: where the driver went and the new install commands.
- package.json: no files, one dependency on the new location, so
  `mpremote mip install github:sparkfun/<old repo>` keeps working and installs
  the current driver.
- examples/package.json (on the default branch) and the old `examples`
  branch's package.json: forward to the new examples manifest.

This only writes files under --output (one folder per old repository). Review
them, then commit each folder's contents to its repository by hand.

Usage:
    make_forwarding_stubs.py [--output forwarding]
"""

import argparse
import json
import os

from qwiic_repo import GITHUB_REPO, REPO_ROOT, load_drivers, normalize_dist_name, read_text

LEGACY = os.path.join(os.path.dirname(__file__), "legacy_repos.json")

README = """# This driver has moved

The SparkFun {name} Python package now lives in the
[Qwiic_Py repository](https://github.com/{repo}/tree/main/{path}),
with every other SparkFun Qwiic Python driver. This repository is archived.

Version 3 changed the API (one snake_case name per method, no properties). See
the [README](https://github.com/{repo}/tree/main/{path}#migrating-from-2x)
for the list of changes. Version 2 stays available from this repository's tags
and from PyPI.

| | Install |
| --- | --- |
| CPython | `pip install {dist}` |
| MicroPython | `mpremote mip install github:{repo}/{path}` |
| CircuitPython | `circup bundle-add {repo}`, then `circup install {main}` |

Please open issues and pull requests in [Qwiic_Py](https://github.com/{repo}/issues).
"""


def manifest(path, version):
    return json.dumps({"urls": [], "deps": [["github:%s/%s" % (GITHUB_REPO, path), "main"]], "version": version}, indent=4) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", default=os.path.join(REPO_ROOT, "forwarding"))
    args = parser.parse_args()

    legacy = json.loads(read_text(LEGACY))
    for driver in load_drivers():
        old_repo = legacy.get(driver.name)
        if not old_repo:
            continue
        out = os.path.join(args.output, old_repo.split("/")[1])
        os.makedirs(os.path.join(out, "examples"), exist_ok=True)
        main_name = (driver.bundle_modules or driver.py_modules or driver.packages)[0]
        with open(os.path.join(out, "README.md"), "w") as f:
            f.write(README.format(name=driver.name, path=driver.rel_path, repo=GITHUB_REPO, dist=normalize_dist_name(driver.dist_name), main=main_name))
        if "micropython" in driver.platforms:
            with open(os.path.join(out, "package.json"), "w") as f:
                f.write(manifest(driver.rel_path, driver.version))
            if driver.example_files():
                text = manifest(driver.rel_path + "/examples", driver.version)
                with open(os.path.join(out, "examples", "package.json"), "w") as f:
                    f.write(text)
                # For the old `examples` branch, whose manifest sits at the root
                with open(os.path.join(out, "examples-branch-package.json"), "w") as f:
                    f.write(text)
        print("wrote", os.path.relpath(out))


if __name__ == "__main__":
    main()
