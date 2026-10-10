import argparse
import sys
from pathlib import Path

from .consolidator import InputDirectoryError, OutputWriteError, consolidate
from .report import format_report


class PortugueseArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, f"Erro nos argumentos: {message}. Use --help para orientações.\n")


def build_parser() -> argparse.ArgumentParser:
    parser = PortugueseArgumentParser(description="Consolida recibos .txt de uma pasta em um CSV.")
    parser.add_argument("--input-dir", help="Pasta que contém os recibos .txt.")
    parser.add_argument("--output", help="Caminho do arquivo CSV que será gerado.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    if not arguments.input_dir or not arguments.output:
        parser.error("informe os argumentos obrigatórios --input-dir e --output")

    try:
        result = consolidate(Path(arguments.input_dir), Path(arguments.output))
    except InputDirectoryError as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 2
    except OutputWriteError as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    print(format_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
