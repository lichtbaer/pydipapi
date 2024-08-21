from setuptools import setup, find_packages

VERSION = '0.0.2'
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
    url="https://github.com/lichtbaer/pydipapi",
    install_requires=["requests", "pydantic"],  # add any additional packages that
    extras_require={
        "pandas": ["pandas"]  # Optional dependencies
    },
    keywords=['Bundestag'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
    ]
)