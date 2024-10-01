from gi.repository import Adw
from gi.repository import Gtk
from UI.MainButtons import MainButtons
from UI.ContainerList import ContainerList

class Sidebar(Gtk.Box):

    def __init__(self):
        super().__init__()
        self.content= Adw.ToolbarView()
        self.content.add_top_bar(self.get_header())
        self.content.set_content(self.get_content())
        self.set_homogeneous(True)
        self.append(self.content)

    def get_header(self):
        header = Adw.HeaderBar()
        header.set_show_title(True)
        return header

    def get_content(self):
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        content.append(MainButtons())
        content.append(ContainerList())
        return content
