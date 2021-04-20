# kubespin

**kubespin** is a very simple tool for easily generating Spinnaker Pipeline Definitions from a manifest file. This is particularly useful if your app is made up by many modules that follows a very similar flow from Development to Production environments.

## Requirements

- Python 3.8+
- jsonnet (Tested with https://github.com/google/jsonnet)

## Development

After you clone the repository, run the following command in kubespin root path:

```bash
python setup.py develop
```

You are ready to go!

## Running examples

The `examples/` path contains some examples on how to take advantage of `kubespin` and `jsonnet`. To try it, run:

```bash
cd examples/
kubespin myapps.json -t ./templates/
```

## The Manifest file

The manifest file is a json file that holds a declaration for your app modules and pipelines.

### Modules

A module is a concept directly mapped to [Spinnaker's application concept](https://spinnaker.io/guides/user/applications/). It holds a piece of your application (a microservice, for instance):

```json
...
"modules": [
        {
            "name": "demo-module",
            "contact": "someone@email.com",
            "description": "A module for demo",
            "properties": {
                "serviceName": "demo-svc",
                "docker": "demo-image",
                "helm": "demo-chart"
            }
        }
    ],
...
```

A module is basically described by its name, a contact for a person responsible for it and a brief description of what it does. You can also rely on `properties` to store `key-value` pairs that will be available in your jsonnet template.

### Pipelines

Pipelines describe actual pipelines that will be applied to all your modules:

```json
...

"pipelines": [
        {
            "type": "deploy",
            "namespace": "qa",
            "properties": {
                "account": "spinnaker-qa-account"
            }
        }
    ]

...
```

It is basically described by a `type` and `namespace` attributes. The `type` holds, in simple terms, the name of the template used to render the pipeline. The `namespace` attribute refers to kubernetes namespace that the pipeline refers to (a deployment to a dev namespace, for instance). The namespace itself can be used to define other types of namespaces, such as AWS Resource Groups.

### The templates

**kubespin** looks for templates in the following structure:

```
./
├── applications/
│   ├── default
│   │   ├── app.jsonnet
└── pipelines/
    ├── default
    │   ├── <type>.jsonnet
    ├── custom_templates
    │   ├── <type>.jsonnet
```

The `applications` folder holds templates for Spinnaker app itself, while the `pipelines` folder holds for Spinnaker pipelines.

The `default` template group can be changed at the module level by adding a `template` attribute:

```json
...
"modules": [
        {
            "name": "demo-module",
            "contact": "someone@email.com",
            "description": "A module for demo",
            "template": "custom_templates",
            "properties": {
                "serviceName": "demo-svc",
                "docker": "demo-image",
                "helm": "demo-chart"
            }
        }
    ],
...
```

This way, instead of looking for templates in `default` folder, **kubespin** will look for templates in the `custom_templates` folder for the module.

#### Context

When rendering the template, the jsonnet will receive a `module` parameter for applications and pipelines and a `pipeline` parameter for pipelines only. This contains the same json defined in the manifest for the module x pipeline being rendered:

```jsonnet
local module = std.extVar('module');
local pipeline = std.extVar('pipeline');

...

local moniker = sponnet.moniker(module.name);
local namespace = pipeline.namespace;

# Docker image 
local dockerArtifact = sponnet.artifacts
    .dockerImage()
    .withName('docker.io/' + module.properties.docker)
    .withReference('docker.io/' + module.properties.docker)
    .withArtifactAccount('docker-registry');
...

```
