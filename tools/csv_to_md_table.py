import csv


def generate_markdown_table(csv_file, output_file):
    # Inicializa a tabela Markdown
    markdown_table = "| Name | Links | Extensions | XLEN | Language | Status | Full Log |\n"
    markdown_table += "| ---- | ------ | ---------- | ---- | -------- | ------ | -------- |\n"

    # Lê o arquivo CSV
    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)

        # Itera sobre cada linha do CSV
        for row in reader:
            name = row.get("Name", "")
            github_link = row.get("Repository", "")
            extensions = row.get("Extensions", "")
            xlen = row.get("XLEN", "")
            language = row.get("Language", "")

            # Links formatados para GitHub e Website
            links = []
            if github_link:
                links.append(f"[Github]({github_link})")

            # Extrai o nome do repositório a partir do link do GitHub
            repo_name = github_link.rstrip("/").split("/")[-1] if github_link else ""

            # Status e Full Log para o Jenkins, com o nome do repositório
            if repo_name:
                status = f"[![Build Status](https://processorci.lsc.ic.unicamp.br/jenkins/buildStatus/icon?job={repo_name})](https://processorci.lsc.ic.unicamp.br/jenkins/blue/organizations/jenkins/{repo_name}/activity)"
                full_log = f"[Log](https://processorci.lsc.ic.unicamp.br/jenkins/blue/organizations/jenkins/{repo_name}/activity)"
            else:
                status = "N/A"
                full_log = "N/A"

            # Adiciona a linha à tabela
            markdown_table += f"| {name} | {', '.join(links)} | {extensions} | {xlen} | {language} | {status} | {full_log} |\n"

    # Salva o markdown gerado em um arquivo
    with open(output_file, mode="w") as output:
        output.write(markdown_table)


if __name__ == "__main__":
    csv_file = "data/processadores.csv"  # Nome do arquivo CSV de entrada
    output_file = "data/processors_table.md"  # Nome do arquivo de saída em Markdown
    generate_markdown_table(csv_file, output_file)
    print(f"Tabela gerada em {output_file}")
