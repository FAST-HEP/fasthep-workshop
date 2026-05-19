from __future__ import annotations

try:
    from ._version import version as __version__  # type: ignore[import-untyped]
except ModuleNotFoundError:
    __version__ = "0+unknown"
