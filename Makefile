# Makefile for project build automation
# Copyright (c) 2026 Johannes Krohn <jkrohn@cisco.com>
# License: MIT

.PHONY: all package docs types clean rst async methref endpointref apib oas oas-hybrid sync-stubs sync-stubs-dry sync-stubs-no-llm sync-stubs-verbose sync-stubs-one
# Default target builds everything
all: clean types methref endpointref async docs package

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
	script/endpoint_ref.py docs/user/method_ref.rst --format rst
methref: docs/user/method_ref.rst

endpoint_ref.md: $(WXC_SDK_PY_FILES)
	@echo "==> Creating endpoint_ref.md"
	script/endpoint_ref.py endpoint_ref.md
endpointref: endpoint_ref.md

clean:
	@echo "==> Cleaning previous build artifacts"
	script/clean

rst:
	@echo "==> Building RST files"
	uv run sphinx-apidoc -o docs/apidoc -f -e -M wxc_sdk 'wxc_sdk/all_types.py'

docs: methref
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
	script/oas2py.py --with-examples --body-style args

oas-hybrid:
	@echo "==> Creating Python sources from OAS files (--body-style hybrid)"
	script/oas2py.py --cleanup
	script/oas2py.py --with-examples --body-style hybrid

sync-stubs:
	@echo "==> Syncing wxc_sdk/ with stub changes (deterministic + LLM)"
	uv run python -m script.sdk_sync

sync-stubs-dry:
	@echo "==> Syncing wxc_sdk/ — dry run, report only"
	uv run python -m script.sdk_sync --dry-run

sync-stubs-no-llm:
	@echo "==> Syncing wxc_sdk/ — deterministic patches only"
	uv run python -m script.sdk_sync --no-llm

sync-stubs-verbose:
	@echo "==> Syncing wxc_sdk/ with stub changes (deterministic + LLM, verbose)"
	uv run python -m script.sdk_sync --verbose

sync-stubs-one:
	@if [ -z "$(STUB)" ]; then echo "Usage: make sync-stubs-one STUB=<basename-or-path>"; exit 2; fi
	@echo "==> Syncing wxc_sdk/ — single stub ($(STUB)), deterministic + LLM, verbose"
	uv run python -m script.sdk_sync --verbose --stub "$(STUB)"
