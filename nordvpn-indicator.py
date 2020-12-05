
# Credit to for a working starter example:
# https://gist.github.com/jmarroyave/a24bf173092a3b0943402f6554a2094d

import os
import gi
import subprocess
import signal
import time
from threading import Thread

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk
from gi.repository import GObject
from gi.repository import AppIndicator3
from gi.repository import Notify

APPINDICATOR_ID = 'nordvpn-indicator'
executable_path = 'nordvpn'
connected_icon_path = 'nordvpn_connected.png'
disconnected_icon_path = 'nordvpn_disconnected.png'
connected_string = "Status: Connected"
disconnected_string = "Status: Disconnected"

poll_frequency = 3

class AppIndicator:
    """Class for system tray icon.
    This class will show status of NordVPN icon in system tray.
    """

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, os.path.realpath(
            disconnected_icon_path), AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.indicator.set_title(APPINDICATOR_ID)
        # run the daemon
        self.daemon = Thread(target=self.__run_daemon)
        self.daemon.setDaemon(True)
        self.daemon.start()

    def __run_daemon(self):
        while True:
            self.handle_nordvpn_status()
            time.sleep(poll_frequency)

    def handle_nordvpn_status(self):
        try:
            status = subprocess.run(
                [executable_path, "status"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if status.returncode != 0:
                Notify.Notification.new(
                    "Execution of nordvpn failed:\n" + status.stdout).show()
                self.quit()
            else:
                # Successful execution. Grep for the connection status.
                if connected_string in status.stdout:
                    self.indicator.set_icon_full(os.path.realpath(connected_icon_path), connected_string)
                elif disconnected_string in status.stdout:
                    self.indicator.set_icon_full(os.path.realpath(disconnected_icon_path), disconnected_string)
                else:
                    Notify.Notification.new(
                        APPINDICATOR_ID + ": Couldn't determine connection status").show()
                    time.sleep(poll_frequency)
        except:
            Notify.Notification.new(
                "Error executing " + executable_path +
                ". Ensure that it is installed and in your PATH").show()
            self.quit()

    def build_menu(self):
        menu = Gtk.Menu()

        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def quit(self):
        Notify.uninit()
        Gtk.main_quit()

def main() -> None:
    # initiaing app indicator
    indicator = AppIndicator()
    Notify.init(APPINDICATOR_ID)
    Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
