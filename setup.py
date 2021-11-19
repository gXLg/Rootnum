import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
  name = "rootnum",
  version = "0.1.1",
  description = "Module for accurate square root operations",
  long_description = README,
  long_description_content_type = "text/markdown",
  url = "https://github.com/gXLg/rootnum",
  author = "dev_null",
  author_email = "natgaev@gmail.com",
  license = "MIT",
  classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
  ],
  packages = ["rootnum"],
  install_requires = [],
)
