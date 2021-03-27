from setuptools import setup, find_packages


if __name__ == "__main__":
    from spotify_recorder.config import __version__ as VERSION

    setup(
        version=VERSION,
        packages=find_packages(),
        entry_points = {
            "console_scripts": ["spotify-rec=spotify_recorder.main:main"],
        }
    )
