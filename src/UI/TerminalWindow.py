from gi.repository import Adw

from Data.Container import Container
from Messaging.Broker import Broker
from Messaging.Events import ContainerAdded
from UI.ApplicationWindow import ApplicationWindow
from UI.Terminal import Terminal


class TerminalWindow(ApplicationWindow):
    def __init__(self, terminal: Terminal, container: Container, *args, **kwargs):
        super().__init__(*args, **kwargs, title=container.name)
        self.terminal = terminal
        self.container = container
        terminal.grab_focus()
        self.cp = self.lookup_action('copy').connect('activate', lambda a, b: self.terminal.on_copy)
        self.pst = self.lookup_action('paste').connect('activate', lambda a, b: self.terminal.on_paste)
        self.set_content(self.get_content())
        self.terminal.connect("child_exited",
                              lambda t, s: self.close())
        self.connect("close-request",
                     lambda _: self.on_close())

    def on_close(self):
        self.terminal.unparent()
        Broker.notify(ContainerAdded(self.container))
        self.close()

    def get_content(self):
        ct = Adw.ToolbarView()
        ct.add_top_bar(Adw.HeaderBar(show_title=True))
        ct.set_content(self.terminal)

        return ct
