"""Shared helpers for the Qwiic_Py repository tools.

Every driver lives in drivers/<name>/ with a pyproject.toml. These helpers read
that metadata so the other tools (package.json generator, checker, registry and
bundle builders) agree on what each driver contains.
"""

import ast
import os
import re
import sys

try:
    import tomllib
except ImportError:  # Python < 3.11
    import tomli as tomllib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRIVERS_DIR = os.path.join(REPO_ROOT, "drivers")
# Shared packages that live at the top level instead of in drivers/
CORE_PACKAGES = ("qwiic_i2c",)
GITHUB_REPO = "sparkfun/Qwiic_Py"
ALL_PLATFORMS = ("cpython", "micropython", "circuitpython")


def read_text(path):
    """The contents of a UTF-8 text file, with the file closed afterwards."""
    with open(path, encoding="utf-8") as f:
        return f.read()


def normalize_dist_name(name):
    """PEP 503 normalized distribution name."""
    return re.sub(r"[-_.]+", "-", name).lower()


def package_path(name):
    """Directory of a package: top level for the core packages, else drivers/<name>."""
    if name in CORE_PACKAGES:
        return os.path.join(REPO_ROOT, name)
    return os.path.join(DRIVERS_DIR, name)


class Driver(object):
    """One package directory (a device driver or qwiic_i2c) and its pyproject.toml metadata."""

    def __init__(self, name):
        self.name = name
        self.path = package_path(name)
        ## Path relative to the repository root, for example drivers/qwiic_bme280
        self.rel_path = os.path.relpath(self.path, REPO_ROOT).replace(os.sep, "/")
        ## True for device drivers, False for the core packages
        self.is_device = name not in CORE_PACKAGES
        with open(os.path.join(self.path, "pyproject.toml"), "rb") as f:
            self.pyproject = tomllib.load(f)
        project = self.pyproject.get("project", {})
        self.dist_name = project.get("name", "")
        self.version = project.get("version", "")
        self.dependencies = project.get("dependencies", [])
        qwiic = self.pyproject.get("tool", {}).get("qwiic", {})
        self.platforms = tuple(qwiic.get("platforms", ALL_PLATFORMS))
        # Modules to install with mip and to ship in the CircuitPython bundle,
        # when a driver has platform-specific modules (qwiic_i2c's backends)
        self.mip_modules = qwiic.get("mip-modules")
        self.bundle_modules = qwiic.get("bundle-modules")
        setuptools = self.pyproject.get("tool", {}).get("setuptools", {})
        self.py_modules = list(setuptools.get("py-modules", []))
        self.packages = list(setuptools.get("packages", []))
        self.package_data = setuptools.get("package-data", {})

    @property
    def tag(self):
        return "%s-%s" % (self.name, self.version)

    @property
    def mip_path(self):
        return "github:%s/%s" % (GITHUB_REPO, self.rel_path)

    def source_files(self, modules=None):
        """Installed files as (installed path, path relative to the driver dir).

        modules limits the single-file modules to that list (see mip-modules).
        """
        files = []
        for module in self.py_modules:
            if modules is not None and module not in modules:
                continue
            files.append((module + ".py", module + ".py"))
        for package in self.packages:
            package_dir = os.path.join(self.path, *package.split("."))
            for name in sorted(os.listdir(package_dir)):
                if name.endswith(".py"):
                    rel = package.replace(".", "/") + "/" + name
                    files.append((rel, rel))
            for pattern in self.package_data.get(package, []):
                data_dir = os.path.dirname(pattern)
                full = os.path.join(package_dir, data_dir)
                suffix = os.path.basename(pattern).replace("*", "")
                for name in sorted(os.listdir(full)):
                    if name.endswith(suffix):
                        rel = "/".join(filter(None, [package.replace(".", "/"), data_dir, name]))
                        files.append((rel, rel))
        return files

    def python_files(self):
        return [rel for _, rel in self.source_files() if rel.endswith(".py")]

    def example_files(self):
        examples = os.path.join(self.path, "examples")
        if not os.path.isdir(examples):
            return []
        return sorted(n for n in os.listdir(examples) if n.endswith(".py"))

    def main_module(self):
        """The module that carries __version__ and the driver class."""
        if self.py_modules:
            return os.path.join(self.path, self.py_modules[0] + ".py")
        if self.packages:
            return os.path.join(self.path, self.packages[0].replace(".", "/"), "__init__.py")
        return None

    def version_files(self):
        """Files that must carry __version__.

        Every single-file module: circup treats each one as a separate library
        and reads its version. A package's version is in its __init__.py.
        """
        if self.py_modules:
            return [os.path.join(self.path, module + ".py") for module in self.py_modules]
        main = self.main_module()
        return [main] if main else []

    def module_version(self, path=None):
        path = path or self.main_module()
        if not path or not os.path.exists(path):
            return None
        tree = ast.parse(read_text(path))
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__version__" for t in node.targets):
                if isinstance(node.value, ast.Constant):
                    return node.value.value
        return None

    def driver_classes(self):
        """Public classes that define available_addresses (the device drivers)."""
        found = []
        for rel in self.python_files():
            tree = ast.parse(read_text(os.path.join(self.path, rel)))
            module = rel[:-3].replace("/", ".")
            if module.endswith(".__init__"):
                module = module[: -len(".__init__")]
            for node in tree.body:
                if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                    for item in node.body:
                        if isinstance(item, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "available_addresses" for t in item.targets):
                            found.append((module, node.name))
        return found


def driver_names():
    """Every package: the core packages, then the device drivers."""
    devices = sorted(
        n for n in os.listdir(DRIVERS_DIR)
        if os.path.isfile(os.path.join(DRIVERS_DIR, n, "pyproject.toml"))
    )
    return list(CORE_PACKAGES) + devices


def load_drivers(names=None):
    return [Driver(n) for n in (names or driver_names())]


def drivers_by_dist_name():
    return {normalize_dist_name(d.dist_name): d for d in load_drivers()}


def requirement_name(requirement):
    """Distribution name of a PEP 508 requirement string."""
    return normalize_dist_name(re.split(r"[\s<>=!~;\[(]", requirement.strip(), 1)[0])


def requirement_marker(requirement):
    return requirement.split(";", 1)[1].strip() if ";" in requirement else ""


def die(message):
    print(message, file=sys.stderr)
    sys.exit(1)
