from typing import Callable

from Kathara.manager.Kathara import Kathara
from gi.repository import Gio, Gtk

from UI.Terminal import Terminal


class GUIManager:
    instance = None

    def __init__(self):
        if self.instance is not None:
            raise Exception("This class is a singleton!")
        GUIManager.instance = self
        self.dialog = Gtk.FileDialog()
        self.dialog.set_title("Select a lab directory")
        self.subscribers: dict[str, list[Callable]] = {
            "lab_started": [],
            "reload": [],
            "set_terminal": [],
            "connect_container": [],
            "detach_container": [],
            "attach_container": [],
            "terminal_exited": [],
            "wipe_terminal": [],
        }

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            return GUIManager()
        return cls.instance

    def subscribe(self, event: str, function: Callable):
        self.subscribers[event].append(function)

    def notify_subscribers(self, event: str, *args):
        print(event, args)
        for subscriber in self.subscribers[event]:
            subscriber(*args)

    def select_lab(self):
        self.dialog.select_folder(callback=self.start_lab)

    def start_lab(self, dialog: Gtk.FileDialog, response_id: Gio.AsyncResult):
        lab = dialog.select_folder_finish(response_id).get_path()
        self.dialog.set_initial_folder(Gio.File.new_for_path(lab))

        term = Terminal()
        term.connect("child_exited", self.on_start_finished)
        term.connect("child_exited", self.on_start_finished)
        self.notify_subscribers("set_terminal", term)
        term.run(["python", "-m", "kathara", "lrestart", "--noterminals", "-d", lab])

    def wipe_all(self):
        term = Terminal()
        term.connect("child_exited", self.on_wipe_finished)
        term.run(
            [
                "python", "-m", "kathara", "wipe",
            ]
        )
        self.notify_subscribers("set_terminal", term)

    def on_start_finished(self, term: Terminal, status: int):
        self.notify_subscribers("lab_started")
        self.reload()

    def on_wipe_finished(self, term: Terminal, status: int):
        self.reload()

    def reload(self):
        containers = Kathara.get_instance().get_machines_api_objects()
        for c in containers:
            print(c.labels)
        containers = [
            (c.labels["name"], c.labels["lab_hash"])
            for c in containers
        ]
        self.notify_subscribers("reload", containers)

    def connect_container(self, container: tuple[str,str]):
        self.notify_subscribers("connect_container", container)

    def detach_container(self, container: tuple[str,str]):
        self.notify_subscribers("detach_container", container)

    def attach_container(self, container: tuple[str,str], term: Terminal):
        self.notify_subscribers("attach_container", container, term)

    def terminal_exited(self, terminal: Terminal, container: tuple[str,str]):
        self.notify_subscribers("terminal_exited", container, terminal)

    def wipe_terminal(self):
        self.notify_subscribers("wipe_terminal")
