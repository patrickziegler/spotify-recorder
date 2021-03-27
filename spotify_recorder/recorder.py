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


import contextlib
import os
import sys

import pyaudio


@contextlib.contextmanager
def _redirect_stderr(to=os.devnull):  # https://stackoverflow.com/a/17954769
    fd = sys.stderr.fileno()

    def _redirect_stderr(to):
        sys.stderr.close()
        os.dup2(to.fileno(), fd)
        sys.stderr = os.fdopen(fd, 'w')

    with os.fdopen(os.dup(fd), 'w') as old_stderr:

        with open(to, 'w') as file:
            _redirect_stderr(to=file)

        try:
            yield

        finally:
            _redirect_stderr(to=old_stderr)


class PyAudioContext:

    def __init__(self):
        self.pya = None

    def __enter__(self):
        with _redirect_stderr():
            self.pya = pyaudio.PyAudio()

        return self.pya

    def __exit__(self, exc_type, exc_val, exc_tb):
        with _redirect_stderr():
            self.pya.terminate()


def get_input_audio_devices():

    with PyAudioContext() as pa:
        k = 0

        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)

            if device_info["maxInputChannels"] > 0:
                yield k, device_info["name"]

                k += 1


def print_all_audio_devices():
    print("Index\tIn\tOut\tName")

    with PyAudioContext() as pa:

        for i in range(pa.get_device_count()):
            device_info = pa.get_device_info_by_index(i)

            print(
                "\t".join(
                    (
                        str(device_info["index"]),
                        str(device_info["maxInputChannels"]),
                        str(device_info["maxOutputChannels"]),
                        str(device_info["name"]),
                    )
                )
            )
