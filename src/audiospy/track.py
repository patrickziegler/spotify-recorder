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


from audiospy.config import ConfigManager
from audiospy.util import redirect_stderr, get_valid_filename
from pydub import AudioSegment
import pyaudio
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
        return "Artist:\t%s\nAlbum:\t%s\nTrack:\t%s\nTitle:\t%s" % (
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


def recorder(config: ConfigManager, track_info: TrackInfo, stop_recording):

    t_start = time.time()
    timeout = float(track_info.length) / 1e6

    with redirect_stderr():
        pa = pyaudio.PyAudio()

    if config.device is None:
        device_index = pa.get_default_input_device_info()["index"]
    else:
        device_index = config.device

    stream = pa.open(
        channels=config.channels,
        format=config.sample_format,
        frames_per_buffer=config.chunk_size,
        input=True,
        input_device_index=device_index,
        rate=config.sample_rate
    )

    frames = []

    while not stop_recording.is_set() and not (time.time() - t_start) > timeout:
        frames.append(stream.read(config.chunk_size))

    stream.stop_stream()
    stream.close()

    with redirect_stderr():
        pa.terminate()

    segment = AudioSegment(
        data=b"".join(frames),
        sample_width=config.sample_size,
        frame_rate=config.sample_rate,
        channels=config.channels
    )

    album_cover = tempfile.NamedTemporaryFile(suffix=".jpg")
    album_cover.write(requests.get(track_info.album_cover_url).content)

    segment.export(
        get_valid_filename(track_info, config.prefix),
        format="mp3",
        bitrate=config.bitrate,
        tags={
            "album": track_info.album_title,
            "album_artist": track_info.album_artist,
            "artist": track_info.track_artist,
            "grouping": track_info.album_disc_number,
            "title": track_info.track_title,
            "track": track_info.track_number,
        },
        cover=album_cover.name
    )
