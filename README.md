# kubespin

**kubespin** is a simple tool for easily generating Spinnaker Pipeline Definitions from a manifest file. This is particularly useful if your app is made up by many modules that follows a very similar pipelines from Development to Production.

## Requirements

- Python 3.8+
- jsonnet

## Development

After you clone the repository, run the following command in kubespin root path:

```bash
python setup.py develop
```

You are ready to go!

## Running examples

The `examples/` path contain some examples on how to take advantage of `kubespin` and `jsonnet`. To try it, run:

```
cd examples/
kubespin myapps.json -t ./templates/
```