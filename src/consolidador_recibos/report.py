from .models import ConsolidationResult


def format_report(result: ConsolidationResult) -> str:
    lines = [
        "Relatório de consolidação",
        f"Arquivos encontrados: {result.found_files}",
        f"Recibos consolidados: {len(result.receipts)}",
        f"Arquivos ignorados: {len(result.ignored_files)}",
        f"CSV gerado em: {result.output_path}",
    ]
    if result.ignored_files:
        lines.append("Arquivos ignorados:")
        lines.extend(f"- {item.filename}: {item.reason}" for item in result.ignored_files)
    return "\n".join(lines)
