from gi.repository import Adw, Gtk

from Logic.GUIManager import GUIManager
from UI.ContentPanel import ContentPanel
from UI.Sidebar import Sidebar


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, titlebar=Gtk.Box(), title="Katharsis")
        self.set_child(self.get_overlay())

    @staticmethod
    def get_overlay():
        overlay = Adw.OverlaySplitView()
        overlay.set_sidebar(Sidebar())
        overlay.set_content(ContentPanel())
        return overlay
