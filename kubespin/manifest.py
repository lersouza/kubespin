import json

from kubespin.domain import Application, Module, Pipeline

def read_application_from_file(filename: str):
    modules = []
    pipelines = []

    application = Application(modules, pipelines)

    with open(filename, "r", encoding="utf-8") as app_file:
        app_config = json.load(app_file)

    for module in app_config["modules"]:
        modules.append(
            Module(**module)
        )

    for pipeline in app_config["pipelines"]:
        pipelines.append(Pipeline(**pipeline))

    
    return application