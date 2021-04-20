from setuptools import setup, find_packages


setup(
    name="kubespin",
    use_scm_version=True,
    url="https://github.com/lersouza/kubespin",
    author="Leandro Rodrigues de Souza",
    license="MIT",
    scripts=["bin/kubespin"],
    include_package_data=True,
    description="A very simple tool to manage an application's lifecycle in Spinnaker.",
    install_requires=["jsonnet"],
    setup_requires=["setuptools_scm"],
    packages=find_packages(),
)