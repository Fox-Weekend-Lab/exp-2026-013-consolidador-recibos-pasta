# Consolidador de Recibos por Pasta

> Este projeto foi gerado automaticamente por IA e revisado por um agente automatizado, nao por uma pessoa. Leia o codigo antes de usar.

## Descrição

Ferramenta em Python que lê arquivos de recibo em texto simples (`.txt`) de uma pasta, extrai os campos rotulados `Data`, `Fornecedor` e `Valor`, e gera um CSV consolidado. Ao fim da execução, apresenta um relatório em português com os arquivos encontrados, consolidados e ignorados.

## Objetivo

Reduzir a transcrição manual de recibos textuais para uma planilha de conferência, registrando apenas dados válidos e informando o motivo de cada arquivo ignorado.

## Como funciona

1. A ferramenta recebe uma pasta de entrada e o caminho do CSV de saída.
2. Considera somente arquivos regulares com extensão `.txt` diretamente na pasta informada, sem percorrer subpastas.
3. Lê cada arquivo usando UTF-8.
4. Procura linhas no formato `Rótulo: valor` para os rótulos `Data`, `Fornecedor` e `Valor`, sem diferenciação entre maiúsculas e minúsculas.
5. Valida a data no formato `DD/MM/AAAA` e o valor como número positivo.
6. Ordena os recibos válidos por data e, em caso de empate, por nome de arquivo.
7. Gera um CSV com as colunas `arquivo`, `data`, `fornecedor` e `valor`.
8. Exibe um relatório com os resultados e, quando houver, a lista de arquivos ignorados.

Os valores aceitam inteiro, decimal com ponto, decimal com vírgula e formato brasileiro com separadores de milhar. O prefixo `R$` também é aceito.

## Arquitetura

- `requirements.txt`: arquivo de dependências do experimento, sem dependências de aplicação.
- `src/consolidador_recibos/__init__.py`: expõe as funções e exceções principais do pacote.
- `src/consolidador_recibos/__main__.py`: implementa a interface de linha de comando e o ponto de entrada do módulo.
- `src/consolidador_recibos/consolidator.py`: percorre a pasta, processa os arquivos `.txt`, ordena recibos e grava o CSV.
- `src/consolidador_recibos/models.py`: define as estruturas de dados para recibos, arquivos ignorados, resultados de parsing e consolidação.
- `src/consolidador_recibos/parser.py`: extrai e valida os campos dos recibos textuais.
- `src/consolidador_recibos/report.py`: formata o relatório final em português.
- `tests/conftest.py`: suporte compartilhado pelos testes.
- `tests/test_cli.py`: testes da interface de linha de comando.
- `tests/test_consolidator.py`: testes da consolidação e geração de CSV.
- `tests/test_parser.py`: testes da extração e validação de recibos.

## Tecnologias

- Python 3.11+
- Biblioteca padrão do Python:
  - `argparse`
  - `csv`
  - `dataclasses`
  - `datetime`
  - `decimal`
  - `pathlib`
  - `re`
- pytest, fornecido pelo ambiente de execução

## Instalação

É necessário ter Python 3.11 ou superior disponível. O experimento não possui dependências de aplicação, portanto não há etapa de instalação de dependências.

O projeto não possui arquivo de instalação Python e o pacote está em `src/`. Por isso, use `PYTHONPATH=src` ao executar o módulo.

## Configuração

O código não lê variáveis de ambiente.

A execução é configurada pelos argumentos obrigatórios:

- `--input-dir`: pasta que contém os arquivos de recibo `.txt`.
- `--output`: caminho do arquivo CSV que será gerado.

## Uso

Em Linux/macOS:

```bash
PYTHONPATH=src python -m consolidador_recibos --input-dir <pasta-de-recibos> --output <caminho-do-arquivo.csv>
```

No Windows (PowerShell):

```powershell
$env:PYTHONPATH="src"; python -m consolidador_recibos --input-dir <pasta-de-recibos> --output <caminho-do-arquivo.csv>
```

Se a pasta de entrada não existir ou não for uma pasta, a execução informa o erro em português e retorna código `2`. Se o CSV não puder ser gravado, retorna código `1`.

## Exemplos

Conteúdo de um recibo válido, por exemplo em um arquivo `.txt`:

```text
Data: 15/03/2024
Fornecedor: Papelaria Exemplo
Valor: R$ 1.234,56
```

Outro formato de valor aceito:

```text
Fornecedor: Serviço Exemplo
Valor: 12.50
Data: 01/04/2024
```

Execução em Linux/macOS:

```bash
PYTHONPATH=src python -m consolidador_recibos --input-dir <pasta-de-recibos> --output <caminho-do-arquivo.csv>
```

O CSV gerado possui o cabeçalho abaixo. Datas são gravadas como `DD/MM/AAAA` e valores com duas casas decimais usando ponto como separador decimal.

```text
arquivo,data,fornecedor,valor
```

Um relatório de execução contém as quantidades de arquivos encontrados, recibos consolidados e arquivos ignorados, além do caminho do CSV. Quando houver arquivos ignorados, o relatório lista o nome e o motivo de cada um.

## Testes

Execute os testes com:

```bash
python -m pytest
```

Os testes não acessam a rede. Eles usam arquivos e diretórios temporários para verificar parsing, consolidação, CSV e comportamento da interface de linha de comando.

## Limitações

- Processa apenas arquivos `.txt` diretamente na pasta de entrada; subpastas não são percorridas.
- Arquivos com outras extensões não são considerados.
- Os únicos campos reconhecidos são `Data`, `Fornecedor` e `Valor`.
- Cada campo deve estar em uma linha no formato `Rótulo: valor`.
- Quando um rótulo aparece mais de uma vez, apenas a primeira ocorrência é usada.
- Datas são aceitas somente no formato `DD/MM/AAAA`.
- O fornecedor é validado apenas quanto à presença de conteúdo.
- Arquivos que não possam ser lidos em UTF-8 são ignorados.
- O CSV é gravado no caminho informado e substitui qualquer conteúdo existente nesse arquivo.
- Não há processamento de PDF, imagens, OCR ou outros formatos de comprovante.

## O que foi aprendido

O experimento demonstra como combinar recursos da biblioteca padrão do Python para automatizar uma consolidação local de arquivos: descoberta determinística com `pathlib`, extração por expressões regulares, validação de datas e valores com `datetime` e `Decimal`, escrita de CSV e comunicação de resultados em português.

Também evidencia a importância de separar registros válidos de arquivos ignorados, preservando o motivo da rejeição para revisão posterior.

## Possível aplicação na FOX

A ferramenta pode apoiar a consolidação de comprovantes administrativos já exportados como texto por processos internos, produzindo um CSV para conferência financeira e identificando arquivos que precisam de correção antes de uma etapa posterior de integração.

## Status

O relatório de testes recebido informa: **7 testes coletados e 7 testes passaram**.
