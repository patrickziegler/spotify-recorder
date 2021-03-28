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

# -------------------------------------------------
# ----->   W O R K   I N   P R O G R E S S   <-----
# -------------------------------------------------

import os
import tempfile
import threading
import time

import requests

from spotify_recorder.track import TrackInfo

# "mpris:artUrl",
# "mpris:length",


class AsyncRecorder:

    def __init__(self, track, config):
        self.config = config
        self.data = None
        self.interrupt = threading.Event()
        self.track = track

    def _record(self):
        print("Start recording:\t%s" % str(self.track))

        while not self.interrupt.is_set():
            time.sleep(0.1)

        filename = self.track.as_filename()
        os.makedirs(self.config.prefix, exist_ok=True)
        with open(os.path.join(self.config.prefix, filename), "w") as fd:
            print("Writing to %s:\t%s" % (filename, str(self.track)))
            fd.write("silence\n")

        print("Done recording:\t%s" % str(self.track))

    def _export(self):
        print("Done exporting:\t%s" % str(self.track))

        # segment = pydub.AudioSegment(
        #    data=b"".join(frames),
        #    sample_width=self.config.sample_size,
        #    frame_rate=self.config.sample_rate,
        #    channels=self.config.channels
        # )

        # segment.export(
        #    get_valid_filename(self, self.config.prefix),
        #    format="mp3",
        #    bitrate=self.config.bitrate,
        #    tags={
        #        "album": self.album_title,
        #        "album_artist": self.album_artist,
        #        "artist": self.track_artist,
        #        "grouping": self.album_disc_number,
        #        "title": self.track_title,
        #        "track": self.track_number,
        #    },
        #    cover=album_cover.name
        # )

        print("Start exporting:\t%s" % str(self.track))

        self.track.cleanup()

    def start(self):

        def _async_run():
            self._record()
            self._export()

        thread = threading.Thread(target=_async_run)
        thread.start()

    def stop(self):
        self.interrupt.set()
