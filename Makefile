# Makefile for project build automation
# Copyright (c) 2026 Johannes Krohn <jkrohn@cisco.com>
# License: MIT

.PHONY: all package docs types async methref apib oas clean rst

# Default target builds everything
all: clean types methref async docs package

# Find all .py files in wxc_sdk (w/ the exception of two auto-generated files)
WXC_SDK_PY_FILES := $(shell find wxc_sdk -mindepth 1 -name '*.py' -not -name 'as_api.py' -not -name 'all_types.py')

wxc_sdk/all_types.py: $(WXC_SDK_PY_FILES)
	@echo "==> Creating types.py"
	python script/all_types.py
types: wxc_sdk/all_types.py

wxc_sdk/as_api.py: wxc_sdk/all_types.py
	@echo "==> Creating as_api.py"
	script/async_gen.py
async: wxc_sdk/as_api.py

docs/user/method_ref.rst: $(WXC_SDK_PY_FILES)
	@echo "==> Creating method_ref.rst"
	script/method_ref.py
methref: docs/user/method_ref.rst

clean:
	@echo "==> Cleaning previous build artifacts"
	script/clean

rst:
	@echo "==> Building RST files"
	uv run sphinx-apidoc -o docs/apidoc -f -e -M wxc_sdk 'wxc_sdk/all_types.py'

docs:
	@echo "==> Building the Docs"
	uv run make -C docs clean
	rm -f docs/apidoc/*.rst
	uv run sphinx-apidoc -o docs/apidoc -f -e -M wxc_sdk 'wxc_sdk/all_types.py'
	uv run make -C docs html

package:
	@echo "==> Building the Source Distribution package"
	rm -rf dist/
	uv build

oas:
	@echo "==> Creating Python sources from OAS files"
	script/oas2py.py --cleanup
	script/oas2py.py --with-examples
