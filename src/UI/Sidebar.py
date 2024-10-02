from gi.repository import Adw, Gtk

from UI.ContainerList import ContainerList
from UI.MainButtons import MainButtons


class Sidebar(Gtk.Box):
    def __init__(self):
        super().__init__(homogeneous=True)
        self.content = Adw.ToolbarView()
        self.content.add_top_bar(self.get_header())
        self.content.add_bottom_bar(MainButtons())
        self.content.set_content(ContainerList())
        self.append(self.content)

    def get_header(self):
        header = Adw.HeaderBar()
        header.set_show_title(True)
        return header
