"""Generate the Markdown table of supported processors from the CSV input."""

import csv

JENKINS_URL = "https://processorci.lsc.ic.unicamp.br/jenkins"


def format_row(row):
    """Return the Markdown table row for a single CSV entry."""
    github_link = row.get("Repository", "")

    # Links formatados para GitHub e Website
    links = f"[Github]({github_link})" if github_link else ""

    # Extrai o nome do repositório a partir do link do GitHub
    repo_name = github_link.rstrip("/").split("/")[-1] if github_link else ""

    # Status e Full Log para o Jenkins, com o nome do repositório
    if repo_name:
        activity = f"{JENKINS_URL}/blue/organizations/jenkins/{repo_name}/activity"
        status = f"[![Build Status]({JENKINS_URL}/buildStatus/icon?job={repo_name})]({activity})"
        full_log = f"[Log]({activity})"
    else:
        status = "N/A"
        full_log = "N/A"

    return (
        f"| {row.get('Name', '')} | {links} | {row.get('Extensions', '')} "
        f"| {row.get('XLEN', '')} | {row.get('Language', '')} "
        f"| {status} | {full_log} |\n"
    )


def generate_markdown_table(csv_file, output_file):
    """Read the processor CSV file and write the Markdown table to disk."""
    # Inicializa a tabela Markdown
    markdown_table = "| Name | Links | Extensions | XLEN | Language | Status | Full Log |\n"
    markdown_table += "| ---- | ------ | ---------- | ---- | -------- | ------ | -------- |\n"

    # Lê o arquivo CSV
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Itera sobre cada linha do CSV
        for row in reader:
            markdown_table += format_row(row)

    # Salva o markdown gerado em um arquivo
    with open(output_file, mode="w", encoding="utf-8") as output:
        output.write(markdown_table)


def main():
    """Generate the table from the default input and output paths."""
    csv_file = "data/processadores.csv"  # Nome do arquivo CSV de entrada
    output_file = "data/processors_table.md"  # Nome do arquivo de saída em Markdown
    generate_markdown_table(csv_file, output_file)
    print(f"Tabela gerada em {output_file}")


if __name__ == "__main__":
    main()
