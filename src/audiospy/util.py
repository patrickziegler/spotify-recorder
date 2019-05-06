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
