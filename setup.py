from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'pydipapi Package - A simple wrapper around the API of the German Bundestag.'

with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()
# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="pydipapi",
    version=VERSION,
    author="JG",
    author_email="<jg@politikpraxis.de>",
    description=DESCRIPTION,
    long_description=description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/gituser/test-tackage",
    install_requires=["requests"],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['Bundestag'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
)