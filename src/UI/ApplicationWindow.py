from gi.repository import Adw, Gio

from Messaging.Broker import Broker
from Messaging.Events import TerminalCopyEvent, TerminalPasteEvent


class ApplicationWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # titlebar=Gtk.Box()
        copy_action = Gio.SimpleAction.new(name="copy", parameter_type=None)
        copy_action.connect("activate", lambda a, b: Broker.notify(TerminalCopyEvent()))
        self.add_action(copy_action)

        paste_action = Gio.SimpleAction.new(name="paste", parameter_type=None)
        paste_action.connect("activate", lambda a, b: Broker.notify(TerminalPasteEvent()))
        self.add_action(paste_action)
