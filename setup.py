from setuptools import setup, find_packages

__version__ = ""

with open("src/audiospy/version.py") as fp:
    exec(fp.read())

setup(
    name="AudioSpy",
    author="Patrick Ziegler",
    license="GPLv3",
    version=__version__,
    packages=find_packages("src"),
    package_dir={"": "src"},
    scripts=["src/scripts/audiospy"]
)
