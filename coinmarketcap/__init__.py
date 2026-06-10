#!/usr/bin/env python
# -*- coding: utf-8 -*-

from importlib.metadata import version, PackageNotFoundError

__title__ = "coinmarketcap"
__author__ = "Jason Byteforge"
__repo__ = "https://github.com/jmazzahacks/byteforge-coinmarketcap"
__license__ = "Apache License 2.0"

try:
    __version__ = version("byteforge-coinmarketcap")
except PackageNotFoundError:
    __version__ = "unknown"

from .core import Market
from .core import ServerException
from .core import MalformedResponseError
from .core import SortOption
from .core import SortDir
from .core import FilterOptions
from .core import AuxFields
