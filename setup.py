#!/usr/bin/env python3
#
# Copyright (C) 2019 Patrick Ziegler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


__version__ = ""

with open("src/spotify_recorder/version.py") as fp:
    exec(fp.read())


if __name__ == "__main__":

    from setuptools import setup, find_packages

    setup(
        name="SpotifyRecorder",
        author="Patrick Ziegler",
        license="GPLv3",
        version=__version__,
        packages=find_packages("src"),
        package_dir={"": "src"},
        scripts=["src/scripts/spotify-rec"]
    )
