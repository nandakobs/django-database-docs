import re

from models_to_puml import get_project_name, make_output_file_editable


def parse_puml_file(file_path):
    parsed_classes = []

    with open(file_path, "r") as file:
        content = file.read()

        classes = re.findall(r'class\s+(\w+)\s+\{([\s\S]*?)\}', content)

        for class_name, class_content in classes:
            if class_name.count('_') <= 1:
                fields = re.findall(r'(\w+):\s+(\w+(\(\d+\))?)(?:\s+)?', class_content)
                parsed_classes.append((class_name, fields))

    return parsed_classes


def generate_markdown(parsed_classes, project_name):
    markdown = f"## {project_name}\n\n"
    markdown += f"LINE_FOR_PROJECT_DESCRIPTION\n\n"
    markdown += "- [Dicionário de Dados](#dicionario-de-dados)\n"

    apps = sorted(set([class_name.split('_')[0] for class_name, _ in parsed_classes]))
    for app_name in apps:
        markdown += f"  - {app_name.lower()}\n"
        app_classes = sorted([class_name for class_name, _ in parsed_classes if class_name.startswith(app_name)])

        for class_name in app_classes:
            markdown += f"      - [{class_name}](#{class_name.lower()})\n"

    markdown += f"\n### Dicionário de Dados <span id=\"dicionario-de-dados\"></span>\n\n"
    markdown += f"LINE_FOR_DATA_DICTIONARY_DESCRIPTION\n\n"

    for app_name in apps:
        app_classes = sorted([class_name for class_name, _ in parsed_classes if class_name.startswith(app_name)])
        for class_name, fields in [item for item in parsed_classes if item[0] in app_classes]:
            markdown += f"#### {class_name} <span id=\"{class_name.lower()}\"></span>\n\n"
            markdown += f"LINE_FOR_MODEL_DESCRIPITION\n\n"
            markdown += "| Campo      | Tipo         | Descrição |\n"
            markdown += "|:-----------|:-------------|:----------|\n"

            for field in fields:
                if field[1] == "timestamp":
                    field = list(field)
                    field[1] = "timestamp with time zone"
                markdown += f"| {field[0]} | {field[1]} |           |\n"

            markdown += "\n"

    return markdown


file_path = "./result.puml"
parsed_classes = parse_puml_file(file_path)

project_name = get_project_name()

markdown_output = generate_markdown(parsed_classes, project_name.capitalize())

with open("data_dict.md", "w") as output_file:
    output_file.write(markdown_output)
make_output_file_editable("./data_dict.md")
