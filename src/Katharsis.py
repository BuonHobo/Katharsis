import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Gio

from UI.Application import Application

app = Application(
    application_id="io.github.buonhobo.UI",
    flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
)
app.run(sys.argv)
