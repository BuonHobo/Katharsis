from Data.Container import Container
from Logic.TerminalManager import TerminalManager
from gi.repository import Adw,Gtk


class ContainerRow(Gtk.Box):
    def __init__(self,container:Container):
        super().__init__()
        self.button_row = Adw.ButtonRow()
        self.container = container
        self.button_row.set_size_request(0, 50)
        self.button_row.connect("activated", self.on_container_row_clicked)
        self.button_row.set_child(self.get_content())
        self.button_row.set_sensitive(container.status == "running")
        self.append(self.button_row)
        self.set_homogeneous(True)

    def get_content(self):
        content = Adw.ButtonContent()
        content.set_icon_name("utilities-terminal-symbolic")
        content.set_label(self.container.name)
        return content

    def on_container_row_clicked(self,btn):
        GUIManager.get_instance().connect_container(self.container)
