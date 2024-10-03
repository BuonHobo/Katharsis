from gi.repository import Adw, Gtk, Gio, GLib

from Logic.GUIManager import GUIManager
from UI.Terminal import Terminal
from UI.ContentPanel import ContentPanel
from UI.Sidebar import Sidebar


from UI.DetachedPanel import DetachedPanel

from Logic.TerminalManager import TerminalManager


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, titlebar=Gtk.Box(), title="Katharsis")
        self.set_child(self.get_overlay())

        self.create_action('copy', Terminal.on_copy, ['<Ctrl><Shift>c'])
        self.create_action('paste', Terminal.on_paste, ['<Ctrl><Shift>v'])
        detach = Gio.SimpleAction.new(name="detach", parameter_type=GLib.VariantType.new_array(GLib.VariantType.new("s")))
        detach.connect("activate", self.on_detach)
        self.add_action(detach)

    @staticmethod
    def get_overlay():
        overlay = Adw.OverlaySplitView()
        overlay.set_sidebar(Sidebar())
        overlay.set_content(ContentPanel())
        return overlay

    def on_detach(self, action, parameter):
        print("Detaching", parameter)
        container = (parameter.get_strv()[0], parameter.get_strv()[1])
        term = TerminalManager.get_instance().get_terminal(container)
        p=DetachedPanel(container=container, term=term)
        p.set_application(self.get_application())
        p.present()

    def create_action(self, name, callback, shortcuts):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
