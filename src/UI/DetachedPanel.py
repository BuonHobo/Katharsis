from gi.repository import Gtk, Adw

from Data.Container import Container
from Logic.GUIManager import GUIManager
from UI.Terminal import Terminal


class DetachedPanel(Gtk.Window):
    def __init__(self, container: Container, term: Terminal):
        super().__init__(title=container.name, titlebar=Gtk.Box())
        self.set_child(Panel(term))
        self.container: Container = container
        self.term: Terminal = term
        GUIManager.get_instance().subscribe("wiped", self.close)
        GUIManager.get_instance().subscribe("terminal_exited", self.on_terminal_exited)

    def do_close_request(self):
        GUIManager.get_instance().attach_container(self.container, self.term)

    def on_terminal_exited(self, container, terminal):
        if container is self.container:
            self.close()


class Panel(Gtk.Box):
    def __init__(self, term: Terminal):
        super().__init__(homogeneous=True)
        self.content = Adw.ToolbarView()
        self.append(self.content)
        self.content.set_content(term)
        self.content.add_top_bar(Adw.HeaderBar(show_title=True))
