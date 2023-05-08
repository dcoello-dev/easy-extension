import re
import os
import sys
import inspect
from string import Template

MODS = ["const", "*", "&"]
SCRIPT_DIR = os.path.dirname(
    os.path.abspath(
        inspect.getfile(
            inspect.currentframe())))


def extract_class_name(file_path):
    with open(file_path) as f:
        text = f.read()
    pattern = r"class .*"
    matches = list(re.finditer(pattern, text))
    if len(matches) > 1:
        print("error more than one class")
        sys.exit(1)

    return str(matches[0].group(0)).split(" ")[1].replace("\n", "")


def extract_pure_virtual_methods(file_path):
    with open(file_path) as f:
        text = f.read()
    pure_virtual_methods = []
    pattern = r"virtual\s+.*\(([^)]*)\)\s.*=\s*0\s*;"
    matches = re.finditer(pattern, text)
    for match in matches:
        pure_virtual_methods.append(match.group(0))
    return pure_virtual_methods


def process_method(method):
    prev, post = method.split("(")
    args = [
        elem.lstrip(" ") for elem in post.split(")")[0].replace(
            "\n", "").split(",") if elem != ""]
    mods = post.split(")")[1].replace(" = 0;", "").split(" ")
    return dict(
        name=prev.split(" ")[-1],
        ret=" ".join(prev.split(" ")[1: -1]),
        args=[dict(type=" ".join(elem.split(" ")[:-1]),
                   name=elem.split(" ")[-1]) for elem in args],
        mods=[elem for elem in mods if elem != ""]
    )


def clean_type(type):
    for t in type.split(" "):
        if t not in MODS:
            return t


def generate_python_method_definition(class_name, method_meta):
    with open(SCRIPT_DIR + "/templates/method.template", "r") as file:
        METHOD_T = Template(file.read())
        types = ",".join([t["name"] for t in method_meta["args"]])
        map_args = "\n".join([clean_type(t["type"]) +
                              " " +
                              t["name"] +
                              " = args[\"" +
                              t["name"] +
                              "\"].get<" +
                              clean_type(t["type"]) +
                              ">();" for t in method_meta["args"]])
        return METHOD_T.safe_substitute(
            dict(CLASS_NAME=class_name,
                 MAP_ARGS=map_args,
                 METHOD=method_meta["name"],
                 ARGS=types))


def generate_python_api(methods):
    with open(SCRIPT_DIR + "/templates/api.template", "r") as file:
        API_T = Template(file.read())
        methods = "\n".join(
            ("{\"" +
             m["name"] +
                "\"," +
                m["name"] +
                "_wrapper, METH_VARARGS, \"\"}," for m in methods))
        return API_T.safe_substitute(dict(METHODS=methods))


def generate_python_main(name):
    with open(SCRIPT_DIR + "/templates/easy_extension.template", "r") as file:
        MAIN_T = Template(file.read())
        return MAIN_T.safe_substitute(dict(NAME=name))


if __name__ == "__main__":
    try:
        file_path = sys.argv[1]
    except IndexError:
        sys.exit(1)

    class_name = extract_class_name(file_path)

    with open(SCRIPT_DIR + "/templates/include.template", "r") as includes:
        print(Template(includes.read()).safe_substitute(NAME=class_name))

    print()
    pure_virtual_methods = extract_pure_virtual_methods(file_path)

    for method in pure_virtual_methods:
        print(generate_python_method_definition(
            class_name, process_method(method)))

    print()

    print(generate_python_api((process_method(p)
          for p in pure_virtual_methods)))

    print()

    print(generate_python_main(class_name))
