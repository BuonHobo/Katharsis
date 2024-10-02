import sys

import gi
from gi.repository import Gio

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Adw
from UI.MainWindow import MainWindow
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

    def create_action(self, name, callback, shortcuts):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
        self.set_accels_for_action(
            detailed_action_name=f'app.{name}',
            accels=shortcuts,
        )


app = MyApp(
    application_id="io.github.buonhobo.Katharsis",
    flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
)
app.run(sys.argv)
