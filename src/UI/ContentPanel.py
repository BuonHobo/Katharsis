from Logic.TerminalManager import TerminalManager
from Logic.GUIManager import GUIManager
from UI.TerminalHeaderTitle import TerminalHeaderTitle
from UI.Terminal import Terminal
from gi.repository import Adw,Gtk

class ContentPanel(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.content = Adw.ToolbarView()
        self.content.add_top_bar(self.get_header())
        self.content.set_content(Terminal())
        self.terminal_manager = TerminalManager()
        GUIManager.get_instance().subscribe("set_terminal",self.set_terminal)
        GUIManager.get_instance().subscribe("connect_container",self.on_connect_container)

        self.append(self.content)

    def get_header(self):
        header = Adw.HeaderBar()
        header.set_title_widget(TerminalHeaderTitle())
        return header

    def set_terminal(self,terminal):
        self.content.set_content(terminal)

    def on_connect_container(self,container):
        terminal = self.terminal_manager.get_terminal(container)
        self.set_terminal(terminal)
