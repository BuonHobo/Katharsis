from gi.repository import Gtk, Adw
from UI.Sidebar import Sidebar
from UI.ContentPanel import ContentPanel

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_titlebar(Gtk.Box())
        self.set_title("KatharaGUI")
        self.set_child(self.get_overlay())

    def get_overlay(self):
        overlay = Adw.OverlaySplitView()
        overlay.set_sidebar(Sidebar())
        overlay.set_content(ContentPanel())
        return overlay
