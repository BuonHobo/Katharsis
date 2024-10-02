from gi.repository import Adw, Gtk

from Logic.GUIManager import GUIManager
from Logic.TerminalManager import TerminalManager
from UI.DetachedPanel import DetachedPanel
from UI.Terminal import Terminal
from UI.TerminalHeaderTitle import TerminalHeaderTitle


class ContentPanel(Gtk.Box):
    def __init__(self):
        super().__init__(homogeneous=True)
        self.terminal_manager = TerminalManager()
        GUIManager.get_instance().subscribe("set_terminal", self.set_terminal)
        GUIManager.get_instance().subscribe(
            "connect_container", self.on_connect_container
        )
        GUIManager.get_instance().subscribe("terminal_exited", self.on_terminal_exited)

        GUIManager.get_instance().subscribe("detach_container", self.on_container_detached)
        GUIManager.get_instance().subscribe("attach_container", self.on_attach_container)

        self.content = self.content = Adw.ToolbarView()
        self.append(self.content)
        self.content.set_content(Terminal())
        self.content.add_top_bar(self.get_header())

    def get_header(self):
        header = Adw.HeaderBar()
        header.set_title_widget(TerminalHeaderTitle())
        return header

    def set_terminal(self, terminal: Terminal):
        if self.content.get_content() is not terminal:
            self.content.set_content(terminal)

    def on_connect_container(self, container):
        terminal = self.terminal_manager.get_terminal(container)
        self.set_terminal(terminal)
        terminal.grab_focus()

    @staticmethod
    def on_new_window_clicked(widget):
        win = Gtk.Window()
        win.set_child(ContentPanel())
        win.set_titlebar(Gtk.Box())
        win.present()

    def on_container_detached(self, container):
        if self.terminal_manager.get_terminal(container).get_parent() is self.content:
            self.content.set_content(Terminal())
            GUIManager.get_instance().wipe_terminal()
        DetachedPanel(container, self.terminal_manager.get_terminal(container)).present()

    def on_attach_container(self, container, term):
        p = term.get_parent()
        if p is None:
            return
        if self.content is p:
            self.content.set_content(Terminal())
            GUIManager.get_instance().wipe_terminal()
        else:
            assert isinstance(p, Adw.ToolbarView)
            p.set_content(Terminal())

    def on_terminal_exited(self, container, term):
        if term.get_parent() is self.content:
            self.content.set_content(Terminal())
            GUIManager.get_instance().wipe_terminal()
        self.terminal_manager.remove_terminal(container)
