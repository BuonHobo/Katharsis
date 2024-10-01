from gi.repository import Adw,Gtk
from Logic.GUIManager import GUIManager


class TerminalHeaderTitle(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.content = Adw.WindowTitle()
        self.content.set_title("")
        GUIManager.get_instance().subscribe("connect_container",self.connect)
        GUIManager.get_instance().subscribe("set_terminal",self.set_terminal)
        self.append(self.content)

    def connect(self,container):
        self.content.set_title(container.name)

    def set_terminal(self,terminal):
        self.content.set_title("")
