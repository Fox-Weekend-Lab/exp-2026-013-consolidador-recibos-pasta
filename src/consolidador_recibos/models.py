from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class Receipt:
    filename: str
    receipt_date: date
    supplier: str
    amount: Decimal


@dataclass(frozen=True)
class IgnoredFile:
    filename: str
    reason: str


@dataclass(frozen=True)
class ParseResult:
    receipt: Receipt | None
    reason: str | None


@dataclass(frozen=True)
class ConsolidationResult:
    found_files: int
    receipts: tuple[Receipt, ...]
    ignored_files: tuple[IgnoredFile, ...]
    output_path: Path
