import csv

import pytest

from consolidador_recibos.consolidator import InputDirectoryError, consolidate


def test_consolidates_only_text_files_in_date_and_filename_order(tmp_path):
    receipts_dir = tmp_path / "receipts"
    receipts_dir.mkdir()
    (receipts_dir / "zeta.txt").write_text("Data: 02/01/2024\nFornecedor: Zeta\nValor: 12.50", encoding="utf-8")
    (receipts_dir / "alpha.txt").write_text("Data: 01/01/2024\nFornecedor: Alpha\nValor: R$ 1.234,56", encoding="utf-8")
    (receipts_dir / "invalid.txt").write_text("Data: 01/01/2024\nFornecedor: Falha", encoding="utf-8")
    (receipts_dir / "ignored.csv").write_text("not a receipt", encoding="utf-8")
    output = tmp_path / "result" / "receipts.csv"

    result = consolidate(receipts_dir, output)

    assert result.found_files == 3
    assert [item.filename for item in result.receipts] == ["alpha.txt", "zeta.txt"]
    assert [(item.filename, item.reason) for item in result.ignored_files] == [("invalid.txt", "campo ausente: valor")]
    with output.open(encoding="utf-8", newline="") as csv_file:
        assert list(csv.reader(csv_file)) == [
            ["arquivo", "data", "fornecedor", "valor"],
            ["alpha.txt", "01/01/2024", "Alpha", "1234.56"],
            ["zeta.txt", "02/01/2024", "Zeta", "12.50"],
        ]


def test_rejects_nonexistent_input_directory_without_creating_csv(tmp_path):
    output = tmp_path / "output.csv"

    with pytest.raises(InputDirectoryError, match="não existe"):
        consolidate(tmp_path / "missing", output)

    assert not output.exists()
