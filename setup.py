import re
import os
import codecs
from setuptools import setup
from setuptools import find_packages


def read(*parts):
    with codecs.open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), "r"
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def required_list():
    with open("requirements.txt", "r") as f:
        required = f.read().splitlines()

    links = []
    del_ls = []
    for i_l in range(len(required)):
        l = required[i_l]
        if l.startswith("git+"):
            links.append(l.split("git+")[-1])
            del_ls.append(i_l)
            required.append(l.split("=")[-1])
    for i_l in del_ls[::-1]:
        del required[i_l]
    return required


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="Graph Server",
    version=find_version("app", "__init__.py"),
    author="Akhilesh Halageri",
    author_email="akhilesh@zetta.ai",
    description="Frontend for serving ChunkedGraph APIs for proofreading.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZettaAI/graph-server",
    packages=find_packages(),
    install_requires=required_list(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)