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
from audiospy.track import TrackInfo, recorder
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
from multiprocessing import Process, Event
import dbus


class DBusWatchdog:

    DBusGMainLoop(set_as_default=True)

    def __init__(self, config=None):
        self._children = []
        self.last_track = None
        self.stop_recording = None

        if config is None:
            self.config = ConfigManager()
        else:
            self.config = config

    def _update(self, *args):
        track_info = TrackInfo(args[1]["Metadata"])

        if track_info == self.last_track:
            return

        self.last_track = track_info

        try:
            self.stop_recording.set()
        except AttributeError:
            pass

        if track_info.is_valid():

            self.stop_recording = Event()

            p = Process(target=recorder, args=(self.config, track_info, self.stop_recording))
            p.start()

            print("Now recording:\n" + str(track_info) + "\n")

            for c in self._children:
                if not c.is_alive():
                    c.join()
                    self._children.remove(c)

            self._children.append(p)

        else:
            print("Ignoring advertisement..." + "\n")

    def _close(self):
        try:
            self.stop_recording.set()
        except AttributeError:
            pass

        for c in self._children:
            c.join()

    def run(self):
        bus = dbus.SessionBus()

        try:
            obj = bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
            obj.connect_to_signal("PropertiesChanged", self._update)

        except dbus.exceptions.DBusException:
            raise EnvironmentError("Spotify is not running!")

        try:
            loop = GLib.MainLoop()
            loop.run()

        except KeyboardInterrupt:
            self._close()
