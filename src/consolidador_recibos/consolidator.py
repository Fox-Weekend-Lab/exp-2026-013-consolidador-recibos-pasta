import csv
from pathlib import Path

from .models import ConsolidationResult, IgnoredFile, Receipt
from .parser import parse_receipt


class InputDirectoryError(ValueError):
    """Raised when the receipt directory cannot be used."""


class OutputWriteError(OSError):
    """Raised when the CSV output cannot be written."""


def consolidate(input_dir: Path, output_path: Path) -> ConsolidationResult:
    """Process direct .txt files from input_dir and write a consolidated CSV."""
    if not input_dir.exists():
        raise InputDirectoryError("A pasta de entrada não existe. Informe uma pasta existente.")
    if not input_dir.is_dir():
        raise InputDirectoryError("A entrada informada não é uma pasta. Use --input-dir com uma pasta.")

    files = sorted(
        (path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() == ".txt"),
        key=lambda path: path.name.casefold(),
    )
    receipts: list[Receipt] = []
    ignored: list[IgnoredFile] = []

    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            ignored.append(IgnoredFile(path.name, "falha ao ler arquivo em UTF-8"))
            continue

        parsed = parse_receipt(content, path.name)
        if parsed.receipt is None:
            ignored.append(IgnoredFile(path.name, parsed.reason or "conteúdo inválido"))
        else:
            receipts.append(parsed.receipt)

    ordered_receipts = sorted(receipts, key=lambda receipt: (receipt.receipt_date, receipt.filename.casefold()))
    _write_csv(output_path, ordered_receipts)
    return ConsolidationResult(
        len(files),
        tuple(ordered_receipts),
        tuple(ignored),
        output_path,
    )


def _write_csv(output_path: Path, receipts: list[Receipt]) -> None:
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["arquivo", "data", "fornecedor", "valor"])
            for receipt in receipts:
                writer.writerow(
                    [
                        receipt.filename,
                        receipt.receipt_date.strftime("%d/%m/%Y"),
                        receipt.supplier,
                        f"{receipt.amount:.2f}",
                    ]
                )
    except OSError as error:
        raise OutputWriteError(
            "Não foi possível gravar o CSV. Verifique o caminho e as permissões de escrita."
        ) from error
