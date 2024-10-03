import sys

import gi
from gi.repository import Gio

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Adw
from UI.MainWindow import MainWindow
from Logic.GUIManager import GUIManager
from UI.Terminal import Terminal

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)
        self.connect("startup", print, "startup")

        self.create_action('copy', Terminal.on_copy, ['<Ctrl><Shift>c'])
        self.create_action('paste', Terminal.on_paste, ['<Ctrl><Shift>v'])

    def on_activate(self, app):
        MainWindow(application=app).present()
        GUIManager.get_instance().reload()

    def create_action(self, name, callback, shortcuts):
        self.set_accels_for_action(
            detailed_action_name=f'win.{name}',
            accels=shortcuts,
        )



app = MyApp(
    application_id="io.github.buonhobo.Katharsis",
    flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
)
app.run(sys.argv)
