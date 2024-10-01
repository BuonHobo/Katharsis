#!/usr/bin/python

import sys

import gi
from Kathara.manager.Kathara import Kathara
from UI.MainWindow import MainWindow

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Adw, GLib, Gtk, Vte


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


def main():
    app = MyApp(application_id="io.github.buonhobo.KatharaGUI")
    app.run(sys.argv)


main()
