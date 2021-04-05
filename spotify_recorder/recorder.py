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
import threading
import time

import pydub
import sounddevice as sd

from spotify_recorder.track import TrackInfo


class AsyncRecorder:

    # static variable for measuring the delay between
    # receiving the signal from dbus and starting
    # to record the track
    t0 = 0

    def __init__(self, track, config):
        self.audio_param = dict()
        self.config = config
        self.frames = list()
        self.interrupt = threading.Event()
        self.track = track

    def _record(self):
        # TODO: make audio device configurable
        with sd.RawInputStream(channels=2, dtype="int16") as stream:
            print("Start recording '%s' (after %.3f s)" %
                  (str(self.track), time.time() - self.t0))
            while not self.interrupt.is_set():
                buffer, _ = stream.read(stream.read_available)
                self.frames.append(buffer)

            self.audio_param["sample_width"] = stream.samplesize
            self.audio_param["frame_rate"] = stream.samplerate
            self.audio_param["channels"] = stream.channels

    def _export(self):
        segment = pydub.AudioSegment(
            data=b"".join([frame[:] for frame in self.frames]),
            **self.audio_param,
        )

        os.makedirs(self.config.prefix, exist_ok=True)
        filepath = os.path.join(self.config.prefix, self.track.as_filename())
        filepath += "." + self.config.format

        segment.export(
            filepath,
            format=self.config.format,
            bitrate=self.config.bitrate,
            tags=self.track.as_dict(),
            cover=self.track.album_cover,
        )

        print("Successfully exported '%s'" % filepath)
        self.track.cleanup()

    def start(self):
        def _async_run():
            self._record()
            self._export()
        thread = threading.Thread(target=_async_run)
        thread.start()

    def stop(self):
        self.interrupt.set()
