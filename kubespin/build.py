import logging
import os

from dataclasses import asdict
from typing import Dict, List

from kubespin.domain import Application, Module, Pipeline
from kubespin.render import render_template


LOGGER = logging.getLogger("builder")
APP_TEMPLATES = ["app.json", "app.jsonnet"]
PIPELINE_TEMPLATES = ["{pipeline_type}.json", "{pipeline_type}.jsonnet"]


class SpinBuildError(Exception):
    pass


def get_template_from_candidates(
    path: str, candidates: List[str], format: Dict[str, str] = None
):
    lookup_table = []

    for template in candidates:
        template_path = template.format(**format) if format else template
        template_file = os.path.join(path, template_path)

        if os.path.exists(template_file) and os.path.isfile(template_file):
            return template_file

        lookup_table.append(template_file)

    raise SpinBuildError(f"No template file found! Tried {lookup_table}")


def build_context_for_app(module: Module):
    return {"module": str(asdict(module))}


def build_context_for_pipeline(module: Module, pipeline: Pipeline):
    return {"module": str(asdict(module)), "pipeline": str(asdict(pipeline))}


def output_asset(asset: str, filename: str, target_dir: str):
    os.makedirs(target_dir, exist_ok=True)  # Ensure build folder is there

    with open(os.path.join(target_dir, filename), "w+", encoding="utf-8") as target:
        target.write(asset)


def build_app(module: Module, base_path: str = "./", target_path: str = "./output/"):
    app_templates_path = os.path.join(base_path, "applications", module.app_template)

    LOGGER.debug(f"About to app definition for module {module.name}.")

    app_context = build_context_for_app(module)
    app_template_file = get_template_from_candidates(app_templates_path, APP_TEMPLATES)

    LOGGER.debug(f"Using template {app_template_file} for build app {module.name}.")

    app_template = render_template(app_template_file, app_context)

    output_asset(app_template, f"app.{module.name}.json", target_path)


def build_pipeline(
    module: Module,
    pipeline: Pipeline,
    base_path: str = "./",
    target_path: str = "./output/",
):
    LOGGER.debug(f"About to build pipeline {pipeline.type} for module {module.name}")

    pipeline_context = build_context_for_pipeline(module, pipeline)
    pipeline_templates = os.path.join(base_path, "pipelines", module.template)

    pipeline_template_file = get_template_from_candidates(
        pipeline_templates, PIPELINE_TEMPLATES, {"pipeline_type": pipeline.type}
    )
    LOGGER.debug(
        f"Using template {pipeline_template_file} for build pipeline {module.name} > {pipeline.type}."
    )

    output_asset(
        render_template(pipeline_template_file, pipeline_context),
        f"{module.name}.{pipeline.namespace}.{pipeline.type}.json",
        target_path,
    )


def build(
    application: Application, base_path: str = "./", target_path: str = "./output/"
):
    LOGGER.info(
        f"Building {len(application.modules)} module(s) with "
        f"{len(application.pipelines)} pipeline(s). "
        f"Output path: {target_path}"
    )

    for module in application.modules:
        LOGGER.debug(f"About to build module {module.name}")

        # build app
        build_app(module, base_path, target_path)

        for pipeline in application.pipelines:
            build_pipeline(module, pipeline, base_path, target_path)
