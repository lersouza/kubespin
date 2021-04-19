import os
import _jsonnet

from typing import Dict


def render_template(file: str, context: Dict[str, str]):
    assert os.path.exists(file)

    if file.endswith(".json"):
        with open(file, "r", encoding="utf-8") as json_file:
            return json_file.read()

    elif file.endswith(".jsonnet"):
        return _jsonnet.evaluate_file(filename=file, ext_codes=context)

    return None