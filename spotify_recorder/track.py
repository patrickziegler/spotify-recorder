# Copyright (C) 2019-2021 Patrick Ziegler
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

import os
import pathlib
import shutil
import tempfile
import uuid

import requests


class TrackInfo:

    DEFAULT_METADATA = {
        "xesam:album": "",
        "xesam:artist": ["", ],
        "xesam:title": "",
    }

    def __init__(self, metadata={}):
        self.album_cover = None
        self.metadata = dict(self.DEFAULT_METADATA)
        self.metadata.update(metadata)

    def getattr(self, key):
        try:
            return self.metadata[key]
        except KeyError:
            return None

    def getattr_joined(self, key, sep=","):
        try:
            return sep.join(self.metadata[key])
        except (KeyError, IndexError):
            return None

    def __eq__(self, other):
        try:
            for key in self.DEFAULT_METADATA:
                if self.metadata[key] != other.metadata[key]:
                    return False
            return True
        except KeyError:
            return False

    def __str__(self):
        return self.getattr("xesam:title")

    def as_dict(self):
        tags = {
            "album": self.getattr("xesam:album"),
            "album_artist": self.getattr_joined("xesam:albumArtist"),
            "artist": self.getattr_joined("xesam:artist"),
            "grouping": self.getattr("xesam:discNumber"),
            "title": self.getattr("xesam:title"),
            "track": self.getattr("xesam:trackNumber"),
        }
        return {k: v for k, v in tags.items() if v is not None}

    def as_filename(self, sep=" - "):
        def _sanitize(s):
            return "".join(c for c in s if c.isalnum() or c in "-_.() ")
        items = [
            self.getattr("xesam:album"),
            self.getattr("xesam:trackNumber"),
            self.getattr("xesam:title"),
        ]
        return sep.join([_sanitize(item) for item in items if item is not None])

    def fetch_album_cover(self):
        if self.album_cover is not None:
            return

        album_cover_url = self.getattr("mpris:artUrl")

        if album_cover_url is None:
            return

        album_cover = os.path.join(
            tempfile.gettempdir(),
            "spotify-rec_album_cover_%s" % uuid.uuid4().hex[:32]
        )

        if album_cover_url.startswith("file://"):
            # TODO: test if file really exists and proper exception handling
            path = album_cover_url[len("file://"):]
            _, ext = os.path.splitext(path)
            album_cover += ext
            shutil.copy2(path, album_cover)

        else:
            # TODO: proper exception handling
            answ = requests.get(album_cover_url).content
            # TODO: find extension in header information of previous request
            album_cover += ".jpg"
            with open(album_cover, "wb") as fd:
                fd.write(answ)

        print("Cached album cover '%s'" % album_cover)
        self.album_cover = album_cover

    def update(self, other):
        self.metadata.update(other.metadata)
        self.fetch_album_cover()

    def is_valid(self):
        return self != TrackInfo()

    def cleanup(self):
        if self.album_cover is not None:
            path = pathlib.Path(self.album_cover)
            path.unlink()
