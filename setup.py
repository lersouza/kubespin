from setuptools import setup, find_packages
from kubespin import VERSION


setup(
    name="kubespin",
    version=VERSION,
    url="https://github.com/lersouza/kubespin",
    author="Leandro Rodrigues de Souza",
    license="MIT",
    scripts=["bin/kubespin"],
    include_package_data=True,
    description="A simple to to manage Spinnaker pipelines declaratively.",
    install_requires=[
        "jsonnet"
    ],
    packages=find_packages()
)