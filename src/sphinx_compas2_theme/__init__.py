from __future__ import print_function

from pathlib import Path
import importlib
import inspect
import sys
import re


__author__ = ["tom van mele"]
__copyright__ = "COMPAS Association"
__license__ = "MIT License"
__email__ = "tom.v.mele@gmail.com"
__version__ = "0.1.5"


default_exclude_patterns = [
    "_build",
    "**.ipynb_checkpoints",
    "_notebooks",
    "**/__temp",
    "**/__old",
]

default_extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.linkcode",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.coverage",
    "sphinx.ext.autodoc.typehints",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_favicon",
    "sphinx_inline_tabs",
    "sphinx_remove_toctrees",
    "sphinx_togglebutton",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
]

default_mock_imports = [
    "System",
    "clr",
    "Eto",
    "Rhino",
    "Grasshopper",
    "scriptcontext",
    "rhinoscriptsyntax",
    "bpy",
    "bmesh",
    "mathutils",
]


def get_linkcode_resolve(organization, repo):
    def linkcode_resolve(domain, info):
        if domain != "py":
            return None
        if not info["module"]:
            return None
        if not info["fullname"]:
            return None

        package = info["module"].split(".")[0]
        if not package.startswith(repo):
            return None

        module = importlib.import_module(info["module"])
        parts = info["fullname"].split(".")

        if len(parts) == 1:
            obj = getattr(module, info["fullname"])
            mod = inspect.getmodule(obj)
            if not mod:
                return None
            filename = mod.__name__.replace(".", "/")
            lineno = inspect.getsourcelines(obj)[1]
        elif len(parts) == 2:
            obj_name, attr_name = parts
            obj = getattr(module, obj_name)
            attr = getattr(obj, attr_name)
            if inspect.isfunction(attr):
                mod = inspect.getmodule(attr)
                if not mod:
                    return None
                filename = mod.__name__.replace(".", "/")
                lineno = inspect.getsourcelines(attr)[1]
            else:
                return None
        else:
            return None

        return f"https://github.com/{organization}/{repo}/blob/main/src/{filename}.py#L{lineno}"

    return linkcode_resolve


def get_latest_version():
    with open("../CHANGELOG.md", "r") as file:
        content = file.read()
        pattern = re.compile(r"## (Unreleased|\[\d+\.\d+\.\d+\])")
        versions = pattern.findall(content)
        latest_version = versions[0] if versions else None
        if latest_version and latest_version.startswith("[") and latest_version.endswith("]"):
            latest_version = latest_version[1:-1]
        return latest_version


def get_html_theme_path():
    theme_path = Path(__file__).parent.absolute()
    return [theme_path]


def get_autosummary_templates_path():
    theme_path = get_html_theme_path()[0]
    templates_path = str(theme_path / "templates")
    return [templates_path]


def get_extensions_path():
    theme_path = get_html_theme_path()[0]
    extensions_path = str(theme_path / "ext")
    return extensions_path


def get_html_static_path():
    theme_path = get_html_theme_path()[0]
    static_path = str(theme_path / "shared" / "static")
    return [static_path]


def skip(app, what, name, obj, would_skip, options):
    if name.startswith("_"):
        return True
    return would_skip


def replace(Klass):
    old_call = Klass.visit_reference

    def visit_reference(self, node):
        if "refuri" in node:
            refuri = node.get("refuri")
            if "generated" in refuri:
                href_anchor = refuri.split("#")
                if len(href_anchor) > 1:
                    href = href_anchor[0]
                    anchor = href_anchor[1]
                    page = href.split("/")[-1]
                    parts = page.split(".")
                    if parts[-1] == "html":
                        pagename = ".".join(parts[:-1])
                        if anchor == pagename:
                            node["refuri"] = href
        return old_call(self, node)

    Klass.visit_reference = visit_reference


def setup(app):
    theme_path = get_html_theme_path()[0]

    app.add_html_theme("multisection", str(theme_path / "multisection"))
    app.add_html_theme("sidebaronly", str(theme_path / "sidebaronly"))


sys.path.append(get_extensions_path())
