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


from audiospy.util import print_available_devices
from audiospy.version import __version__
import pyaudio
import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Monitoring Spotify on D-Bus for recording currently played music")
    parser.add_argument("prefix", type=str, nargs='?', default="", help="Output folder (optional)")
    parser.add_argument("-b", "--bitrate", type=str, dest="bitrate", default="128k", help="MP3 Bitrate")
    parser.add_argument("-d", "--device", type=int, dest="device", default=None, help="Audio device index")
    parser.add_argument("--list-devices", dest="list_devices", action="store_true", default=False, help="Print list of available audio devices")
    parser.add_argument("-v", "--version", action='version', version="AudioSpy v" + __version__ + ", Copyright (C) 2019 Patrick Ziegler")
    args = parser.parse_args()

    if args.list_devices:
        print_available_devices()
        sys.exit()

    return args


class ConfigManager:

    def __init__(self, args=None):
        if args is None:
            args = parse_args()

        self.channels = 2
        self.chunk_size = 1024
        self.bitrate = args.bitrate
        self.device = args.device
        self.prefix = args.prefix
        self.sample_rate = 44100
        self.sample_format = pyaudio.paInt16
        self.sample_size = pyaudio.get_sample_size(self.sample_format)