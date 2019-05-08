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


from pydub import AudioSegment
from spotify_recorder.util import PyAudioContext, get_valid_filename
import requests
import tempfile
import time


class TrackInfo:

    _main_keys = (
        "album_artist",
        "album_disc_number",
        "album_title",
        "track_artist",
        "track_number",
        "track_title"
    )

    config = None

    def __init__(self, meta):
        self.album_artist = meta["xesam:albumArtist"][0]
        self.album_cover_url = meta["mpris:artUrl"]
        self.album_disc_number = meta["xesam:discNumber"]
        self.album_title = meta["xesam:album"]
        self.length = int(meta["mpris:length"])
        self.track_artist = meta["xesam:artist"][0]
        self.track_number = meta["xesam:trackNumber"]
        self.track_title = meta["xesam:title"]

    def __eq__(self, other):
        try:
            for k in TrackInfo._main_keys:
                if getattr(self, k) != getattr(other, k):
                    return False
            return True

        except AttributeError:
            return False

    def __str__(self):
        return "Artist:\t\t%s\nAlbum title:\t%s\nTrack title:\t%s\nTitle number:\t%s" % (
            self.track_artist,
            self.album_title,
            self.track_number,
            self.track_title
        )

    def is_valid(self):
        try:
            for k in TrackInfo._main_keys:
                if getattr(self, k) == "":
                    return False
            return True

        except AttributeError:
            return False

    def record(self, stop_recording):

        frames = []
        t_start = time.time()
        timeout = float(self.length) / 1e6

        with PyAudioContext() as pa:

            if self.config.device is None:
                device_index = pa.get_default_input_device_info()["index"]
            else:
                device_index = self.config.device

            stream = pa.open(
                channels=self.config.channels,
                format=self.config.sample_format,
                frames_per_buffer=self.config.chunk_size,
                input=True,
                input_device_index=device_index,
                rate=self.config.sample_rate
            )

            while not stop_recording.is_set() and not (time.time() - t_start) > timeout:
                frames.append(stream.read(self.config.chunk_size))

            stream.stop_stream()
            stream.close()

        album_cover = tempfile.NamedTemporaryFile(suffix=".jpg")
        album_cover.write(requests.get(self.album_cover_url).content)

        segment = AudioSegment(
            data=b"".join(frames),
            sample_width=self.config.sample_size,
            frame_rate=self.config.sample_rate,
            channels=self.config.channels
        )

        segment.export(
            get_valid_filename(self, self.config.prefix),
            format="mp3",
            bitrate=self.config.bitrate,
            tags={
                "album": self.album_title,
                "album_artist": self.album_artist,
                "artist": self.track_artist,
                "grouping": self.album_disc_number,
                "title": self.track_title,
                "track": self.track_number,
            },
            cover=album_cover.name
        )
