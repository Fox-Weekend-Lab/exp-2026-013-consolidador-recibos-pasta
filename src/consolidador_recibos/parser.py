import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

from .models import ParseResult, Receipt

_FIELD_PATTERN = re.compile(r"^\s*(data|fornecedor|valor)\s*:\s*(.*?)\s*$", re.IGNORECASE)
_DATE_PATTERN = re.compile(r"^\d{2}/\d{2}/\d{4}$")
_BRAZILIAN_AMOUNT_PATTERN = re.compile(r"^(?:\d{1,3}(?:\.\d{3})*|\d+),\d{1,2}$")
_DOT_AMOUNT_PATTERN = re.compile(r"^\d+\.\d{1,2}$")
_INTEGER_AMOUNT_PATTERN = re.compile(r"^\d+$")


def parse_receipt(content: str, filename: str) -> ParseResult:
    """Extract one receipt from labeled text content."""
    fields: dict[str, str] = {}
    for line in content.splitlines():
        match = _FIELD_PATTERN.match(line)
        if match and match.group(1).casefold() not in fields:
            fields[match.group(1).casefold()] = match.group(2).strip()

    for field in ("data", "fornecedor", "valor"):
        if not fields.get(field):
            return ParseResult(None, f"campo ausente: {field}")

    receipt_date = _parse_date(fields["data"])
    if receipt_date is None:
        return ParseResult(None, "data inválida")

    amount = _parse_amount(fields["valor"])
    if amount is None:
        return ParseResult(None, "valor inválido")
    if amount <= 0:
        return ParseResult(None, "valor não positivo")

    return ParseResult(
        Receipt(filename, receipt_date, fields["fornecedor"], amount),
        None,
    )


def _parse_date(value: str):
    if not _DATE_PATTERN.fullmatch(value):
        return None
    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        return None


def _parse_amount(value: str) -> Decimal | None:
    cleaned = value.strip()
    if cleaned.casefold().startswith("r$"):
        cleaned = cleaned[2:].strip()

    sign = ""
    if cleaned[:1] in {"+", "-"}:
        sign, cleaned = cleaned[:1], cleaned[1:]

    if _BRAZILIAN_AMOUNT_PATTERN.fullmatch(cleaned):
        normalized = cleaned.replace(".", "").replace(",", ".")
    elif _DOT_AMOUNT_PATTERN.fullmatch(cleaned) or _INTEGER_AMOUNT_PATTERN.fullmatch(cleaned):
        normalized = cleaned
    else:
        return None

    try:
        return Decimal(sign + normalized)
    except InvalidOperation:
        return None
