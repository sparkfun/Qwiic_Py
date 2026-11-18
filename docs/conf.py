# Sphinx configuration for the Qwiic_Py landing site (qwiic-py.readthedocs.io).
#
# The site is the repository README plus a generated index of every driver
# (docs/drivers.md, written by tools/gen_registry.py). Each driver's API
# reference is built with Doxygen (tools/build_docs.py) and published at
# docs.sparkfun.com/Qwiic_Py/<driver>/.

project = "SparkFun Qwiic Python"
author = "SparkFun Electronics"
copyright = "2019-2026, SparkFun Electronics"

extensions = ["myst_parser"]
source_suffix = {".md": "markdown"}
master_doc = "index"
exclude_patterns = ["_build", "doxygen"]

# GitHub-style heading ids, so README links like (#supported-platforms) work
# here exactly as they do on GitHub
myst_heading_anchors = 3

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
myst_heading_slug_func = "github_slug.github_slug"
myst_enable_extensions = ["colon_fence"]

# The README links to repository files; they live outside the docs tree
suppress_warnings = ["myst.xref_missing"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
