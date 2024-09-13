# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'wxc_sdk'
copyright = '2024, Johannes Krohn'
author = 'Johannes Krohn'

# The full version, including alpha/beta/rc tags
release = '1.22.1'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    # 'autoapi.extension',
    # 'enum_tools.autoenum'
]

# intersphinx allows to reference other RTD projects
# to view an object inventory:
#   python -m sphinx.ext.intersphinx https://dateutil.readthedocs.io/en/stable/objects.inv
intersphinx_mapping = {
    'dateutil': ('https://dateutil.readthedocs.io/en/stable/', None)
}

# We recommend adding the following config value.
# Sphinx defaults to automatically resolve *unresolved* labels using all your Intersphinx mappings.
# This behavior has unintended side-effects, namely that documentations local references can
# suddenly resolve to an external location.
# See also:
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
# intersphinx_disabled_reftypes = ["*"]


# This value selects what content will be inserted into the main body of an autoclass directive.
# both: Both the class’ and the __init__ method’s docstring are concatenated and inserted.
# init: Only the __init__ method’s docstring is inserted.
# class: Only the class’ docstring is inserted. This is the default.
autoclass_content = 'class'

# This value selects if automatically documented members are sorted alphabetical (value 'alphabetical'), by member
# type (value 'groupwise') or by source order (value 'bysource'). The default is alphabetical.
autodoc_member_order = 'bysource'

# autoapi_dirs = ['../wxc_sdk']
# autoapi_keep_files = True
# autoapi_generate_api_docs = True
# autoapi_options = ['show-inheritance']
# autoapi_add_toctree_entry = False
# autoapi_python_class_content = 'both'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


def skip_member(app, what, name, obj, skip, options):
    # skip doc creation for model_config and model_fields members; part of pydantic.BaseModel
    if name in {'model_config', 'model_fields', 'model_computed_fields'}:
        return True
    return None


# def process_bases(app, name, obj, options, bases):
#     # we don't want to document ApiModel as a Base
#     remove_base_index = next((i for i, base in enumerate(bases)
#                               if base.__name__.split('.')[-1] in {'ApiModel'}),
#                              None)
#     if remove_base_index is not None:
#         bases.pop(remove_base_index)
#     print(f'{name=}, {obj.__class__.__name__ =} bases: {", ".join(f"{b}" for b in bases)}')


def setup(app):
    app.connect('autodoc-skip-member', skip_member)
    # app.connect('autodoc-process-bases', process_bases)
