from gi.repository import Gtk, Adw, Gio

from Logic.GUIManager import GUIManager
from UI.Terminal import Terminal


class DetachedPanel(Gtk.ApplicationWindow):
    def __init__(self, container: tuple[str,str], term: Terminal):
        super().__init__(title=container[0], titlebar=Gtk.Box())
        self.set_child(Panel(term))
        self.container: tuple[str,str] = container
        self.term: Terminal = term
        GUIManager.get_instance().subscribe("terminal_exited", self.on_terminal_exited)

        self.create_action('copy', Terminal.on_copy, ['<Ctrl><Shift>c'])
        self.create_action('paste', Terminal.on_paste, ['<Ctrl><Shift>v'])


    def do_close_request(self):
        GUIManager.get_instance().attach_container(self.container, self.term)

    def on_terminal_exited(self, container, terminal):
        print("closed")
        if container == self.container:
            print("closed")
            self.close()

    def create_action(self, name, callback, shortcuts):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)


class Panel(Gtk.Box):
    def __init__(self, term: Terminal):
        super().__init__(homogeneous=True)
        self.content = Adw.ToolbarView()
        self.append(self.content)
        self.content.set_content(term)
        self.content.add_top_bar(Adw.HeaderBar(show_title=True))
