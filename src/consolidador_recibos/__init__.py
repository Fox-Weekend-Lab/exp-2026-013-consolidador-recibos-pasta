"""Ferramentas para consolidar recibos textuais em CSV."""

from .consolidator import InputDirectoryError, OutputWriteError, consolidate
from .parser import parse_receipt

__all__ = ["InputDirectoryError", "OutputWriteError", "consolidate", "parse_receipt"]
