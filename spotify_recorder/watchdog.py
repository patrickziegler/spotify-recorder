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

import time

import pydbus
from gi.repository import GLib

from spotify_recorder.recorder import AsyncRecorder
from spotify_recorder.track import TrackInfo


def bus_name_filter_default(names):
    """Selecting the bus name to be used for monitoring

    This filter prefers the spotify client (if found) over firefox
    and will throw an error if multiple firefox instances (or none
    at all) were found

    Args:
        names (list of str): candidates to chose from

    Return:
        the chosen bus name as str
    """

    # TODO: also check for other browsers / integrations
    firefox_instances = list()

    for name in names:
        if "spotify" in name:
            return name
        elif "firefox" in name:
            firefox_instances.append(name)

    if len(firefox_instances) > 1:
        raise EnvironmentError("Multiple firefox dbus instances found")

    try:
        return firefox_instances[0]
    except IndexError:
        raise EnvironmentError("No mpris interface found")


class DBusWatchdog:

    def __init__(self, config):
        self.current_track = TrackInfo()
        self.current_recorder = AsyncRecorder(self.current_track, config)
        self.config = config

    def on_properties_changed(self, interface, properties, *args):
        AsyncRecorder.t0 = time.time()

        try:
            track = TrackInfo(properties["Metadata"])
        except KeyError:
            return

        if track == self.current_track:
            self.current_track.update(track)
            return

        self.current_track = track
        self.current_recorder.stop()

        if not track.is_valid():
            print("Ignoring ads.." + "\n")
            return

        print("New track '%s' is playing" % str(track))

        # TODO: will the previous object be garbage collected while `stop` is still being executed?
        self.current_recorder = AsyncRecorder(track, self.config)
        self.current_recorder.start()

    def close(self):
        self.current_recorder.stop()

    def watch(self, bus=None, bus_name_filter=None):
        if bus is None:
            bus = pydbus.SessionBus()

        if bus_name_filter is None:
            bus_name_filter = bus_name_filter_default

        bus_name_candidates = [name for name in bus.get(
            ".DBus").ListNames() if "mpris" in name]
        bus_name = bus_name_filter(bus_name_candidates)

        print("Watchdog is monitoring '%s'" % bus_name)

        mpris = bus.get(bus_name, "/org/mpris/MediaPlayer2")
        mpris.PropertiesChanged.connect(self.on_properties_changed)

        try:
            loop = GLib.MainLoop()
            loop.run()

        except KeyboardInterrupt:
            self.close()
