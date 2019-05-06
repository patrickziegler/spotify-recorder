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


from contextlib import contextmanager
import os
import pyaudio
import sys


@contextmanager
def redirect_stderr(to=os.devnull):
    """
    https://stackoverflow.com/a/17954769
    """
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


def print_available_devices():
    print("Available audio devices (by index):")

    with redirect_stderr():
        pa = pyaudio.PyAudio()

    for i in range(pa.get_device_count()):
        device_info = pa.get_device_info_by_index(i)
        print(str(device_info["index"]) + "\t" + str(device_info["name"]))

    pa.terminate()


def skip_invalid_chars(s):
    return "".join(c for c in s if c.isalnum() or c in "-_.() ")


def get_valid_filename(track_info, prefix=""):

    new_file = skip_invalid_chars(
        " - ".join(
            (
                str(track_info.track_number),
                str(track_info.track_title)
            )
        )
    )

    if prefix == "":
        new_folder = skip_invalid_chars(str(track_info.album_title))
    else:
        new_folder = os.sep.join(
            (
                os.path.abspath(os.path.expanduser(prefix)),
                skip_invalid_chars(str(track_info.album_title))
            )
        )

    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    return os.sep.join(
        (
            new_folder,
            new_file + ".mp3"
        )
    )
