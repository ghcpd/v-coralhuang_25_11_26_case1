"""Deprecated: the original implementation has moved to `user_display_original.py`.

This module re-exports the original functions for backward compatibility.
"""

# pylint: disable=wildcard-import
from user_display_original import *  # type: ignore

__all__ = [name for name in globals() if not name.startswith("_")]
