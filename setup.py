from setuptools import setup, find_packages


setup(
    name="kubespin",
    use_scm_version=True,
    url="https://github.com/lersouza/kubespin",
    author="Leandro Rodrigues de Souza",
    license="MIT",
    scripts=["bin/kubespin"],
    include_package_data=True,
    description="A simple to to manage Spinnaker pipelines declaratively.",
    install_requires=["jsonnet"],
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
)