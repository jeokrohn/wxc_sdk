# -*- coding: utf-8 -*-
"""IPython Project Console.

Used to interactively work with the main package contents in IPython.
"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *

import wxc_sdk

__copyright__ = "Copyright (c) 2022 Johannes Krohn <jkrohn@cisco.com>"
__license__ = "MIT"


api = wxc_sdk.WebexSimpleApi()
