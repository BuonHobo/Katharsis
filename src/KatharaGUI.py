import sys

import gi
from gi.repository import Gio

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Adw
from UI.MainWindow import MainWindow


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        MainWindow(application=app).present()


app = MyApp(
    application_id="io.github.buonhobo.KatharaGUI",
    flags=Gio.ApplicationFlags.NON_UNIQUE,
)
app.run(sys.argv)
