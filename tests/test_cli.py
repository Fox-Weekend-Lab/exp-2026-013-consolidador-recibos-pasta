from consolidador_recibos.__main__ import main


def test_cli_prints_portuguese_report(tmp_path, capsys):
    receipts_dir = tmp_path / "receipts"
    receipts_dir.mkdir()
    (receipts_dir / "receipt.txt").write_text(
        "Data: 10/03/2024\nFornecedor: Mercado\nValor: 20,00",
        encoding="utf-8",
    )
    output = tmp_path / "output.csv"

    exit_code = main(["--input-dir", str(receipts_dir), "--output", str(output)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Relatório de consolidação" in captured.out
    assert "Recibos consolidados: 1" in captured.out
    assert captured.err == ""
    assert output.exists()


def test_cli_returns_nonzero_for_invalid_directory(tmp_path, capsys):
    exit_code = main(["--input-dir", str(tmp_path / "missing"), "--output", str(tmp_path / "out.csv")])
    captured = capsys.readouterr()

    assert exit_code != 0
    assert "pasta de entrada não existe" in captured.err
