from setuptools import setup, find_packages


if __name__ == "__main__":
    version = {}

    with open("src/spotify_recorder/version.py") as fp:
        exec(fp.read(), version)

    setup(
        version=version["__version__"],
        packages=find_packages("src"),
        package_dir={"": "src"},
        scripts=["src/app/spotify-rec.py"]
    )
