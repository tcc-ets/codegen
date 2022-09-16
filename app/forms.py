from typing import List
from rich import print
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class Field:
    def __init__(self, name, type) -> None:
        self.name = name
        if type:
            self.input_type = type
        else:
            self.input_type = "text"

        self.type = self.get_type()
        self.initial_value = self.get_initial_value()

    def get_type(self):
        match self.input_type:
            case "text":
                return "string"
            case "email":
                return "string"
            case "number":
                return "number"
            case "pass":
                self.input_type = "password"
                return "string"
            case "date":
                return "Date"

    def get_initial_value(self):
        match self.type:
            case "string":
                return "''"
            case "number":
                return "0"
            case "Date":
                return "new Date()"


def get_base(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def fields_to_jsx(fields: List[Field]) -> str:
    jsx_list = []
    for field in fields:
        line = f'<label htmlFor="{field.name}">{field.name.capitalize()}</label>\n\t\t    <Field id="{field.name}" type={field.input_type} name="{field.name}" placeholder={field.name} />'
        jsx_list.append(line)
    return "\n\t\t    ".join(jsx_list)


def fields_to_interface(fields: List[Field]) -> str:
    types_list = []
    for field in fields:
        line = f"{field.name}: {field.type}"
        types_list.append(line)
    return "\n    ".join(types_list)


def fields_to_values(fields: List[Field]) -> str:
    types_list = []
    for field in fields:
        line = f"{field.name}: {field.initial_value}"
        types_list.append(line)
    return "\n\t\t    ".join(types_list)


def generate_form(name: str, _fields: str):

    fields = []
    for field in _fields.split(","):
        field = field.split(":")
        fields.append(Field(name=field[0], type=field[1] if 1 < len(field) else None))

    content = (
        get_base(f"{dir_path}/../bases/Form.txt")
        .replace("%FORM_NAME%", name.capitalize())
        .replace("%INPUTS_JSX%", fields_to_jsx(fields))
        .replace("%INPUTS_INTERFACE%", fields_to_interface(fields))
        .replace("%INITIAL_VALUES%", fields_to_values(fields))
    )

    filename = f"./src/forms/{name.capitalize()}.tsx"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
