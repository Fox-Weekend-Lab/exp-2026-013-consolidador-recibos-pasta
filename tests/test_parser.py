from datetime import date
from decimal import Decimal

from consolidador_recibos.parser import parse_receipt


def test_parses_valid_receipt_with_comma_amount():
    result = parse_receipt("Data: 05/02/2024\nFornecedor: Papelaria Sol\nValor: 12,50\n", "a.txt")

    assert result.reason is None
    assert result.receipt is not None
    assert result.receipt.receipt_date == date(2024, 2, 5)
    assert result.receipt.supplier == "Papelaria Sol"
    assert result.receipt.amount == Decimal("12.50")


def test_parses_case_insensitive_labels_in_any_order():
    result = parse_receipt("vAlOr : R$ 1.234,56\nFORNECEDOR: Loja Azul\ndAtA: 01/12/2023", "b.txt")

    assert result.receipt is not None
    assert result.receipt.receipt_date == date(2023, 12, 1)
    assert result.receipt.amount == Decimal("1234.56")


def test_reports_missing_and_invalid_fields():
    assert parse_receipt("Fornecedor: Loja\nValor: 10", "a.txt").reason == "campo ausente: data"
    assert parse_receipt("Data: 31/02/2024\nFornecedor: Loja\nValor: 10", "a.txt").reason == "data inválida"
    assert parse_receipt("Data: 01/01/2024\nFornecedor: Loja\nValor: texto", "a.txt").reason == "valor inválido"
    assert parse_receipt("Data: 01/01/2024\nFornecedor: Loja\nValor: 0", "a.txt").reason == "valor não positivo"
