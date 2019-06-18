import logging

import utility
import buffers
import window

# from dbus.mainloop.glib import DBusGMainLoop
import dbus
import dbus.service
from dbus.mainloop.pyqt5 import DBusQtMainLoop
from PyQt5.QtWidgets import QApplication

logging.basicConfig(level=logging.INFO)

"""
This is a Next port with Qt's Web Engine, through PyQt.

It is possible to test this from the Python or the Lisp REPL.

To send commands to the web engine from Lisp:
- start the PyQt port (make run)
- start lisp, quickload next
- start and initialize the lisp side:

    (in-package :next)
    (start)

this creates an `*interface*` object.
Now you can use any built-in methods such as (window-make *interface*).
"""

PLATFORM_PORT_OBJECT_PATH = "/engineer/atlas/next/platform"
PLATFORM_PORT_NAME = "engineer.atlas.next.platform"


class DBusWindow(dbus.service.Object):
    # Lisp core dbus proxy.
    core_dbus_proxy = None

    def __init__(self, conn, object_path=PLATFORM_PORT_OBJECT_PATH, core_dbus_proxy=None):
        dbus.service.Object.__init__(self, conn, object_path)
        self.core_dbus_proxy = core_dbus_proxy

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='s')
    def window_make(self, window_id):
        return window.make(window_id)

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='ss')
    def window_set_title(self, window_id, title):
        _window = window.get_window(window_id)
        return _window.set_title(title)

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='s')
    def window_delete(self, window_id):
        _window = window.get_window(window_id)
        return _window.delete()

    @dbus.service.method(PLATFORM_PORT_NAME)
    def window_active(self):
        return window.active()

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='s')
    def window_exists(self, window_id):
        try:
            _window = window.get_window(window_id)
            return _window.exists()
        except Exception:
            return False

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='ss')
    def window_set_active_buffer(self, window_id, buffer_id):
        _window = window.get_window(window_id)
        _buffer = buffers.get_buffer(buffer_id)
        return _window.set_active_buffer(_buffer)

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='si')
    def window_set_minibuffer_height(self, window_id, height):
        _window = window.get_window(window_id)
        return _window.set_minibuffer_height(height)

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='s')
    def buffer_make(self, buffer_id):
        return buffers.make(buffer_id)

    @dbus.service.method(PLATFORM_PORT_NAME)
    def buffer_delete(self, buffer_id):
        _buffer = buffers.get_buffer(buffer_id)
        return _buffer.delete()

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='ss')
    def buffer_load(self, buffer_id, url):
        _buffer = buffers.get_buffer(buffer_id)
        return _buffer.load(url)

    @dbus.service.method(PLATFORM_PORT_NAME)
    def buffer_evaluate_javascript(self, buffer_id, script):
        _buffer = buffers.get_buffer(buffer_id)
        return _buffer.evaluate_javascript(script)

    @dbus.service.method(PLATFORM_PORT_NAME, in_signature='ss')
    def minibuffer_evaluate_javascript(self, window_id, script):
        _window = window.get_window(window_id)
        return _window.minibuffer_evaluate_javascript(script)

    @dbus.service.method(PLATFORM_PORT_NAME)
    def generate_input_event(self):
        pass
        # utility.generate_input_event()

    #  DEVELOPER HELP FUNCTION
    @dbus.service.method(PLATFORM_PORT_NAME)
    def window_killall(self):
        return utility.killall()

    #  DEVELOPER HELP FUNCTION
    @dbus.service.method(PLATFORM_PORT_NAME)
    def window_list(self):
        return utility.list_windows()


def main():
    app = QApplication([])
    DBusQtMainLoop(set_as_default=True)
    # DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    # name/dbuswindow MUST be defined even if not used.
    name = dbus.service.BusName('engineer.atlas.next.platform', session_bus)  # noqa: F841
    # CORE_INTERFACE = "engineer.atlas.next.core"
    # CORE_OBJECT_PATH = "/engineer/atlas/next/core"
    # core_dbus_proxy = session_bus.get_object(CORE_INTERFACE, CORE_OBJECT_PATH)
    dbuswindow = DBusWindow(session_bus)  # noqa: F841
    app.exec_()


if __name__ == '__main__':
    main()
