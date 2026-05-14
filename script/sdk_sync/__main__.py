"""Entry point for ``python -m script.sdk_sync``.

Delegates to :func:`script.sdk_sync.driver.main`. This thin shim exists so
the package is invocable directly as a module while keeping
:mod:`script.sdk_sync.driver` importable for tests.
"""

import sys

from .driver import main

sys.exit(main())
