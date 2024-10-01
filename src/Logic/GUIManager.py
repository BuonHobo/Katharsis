from pathlib import Path
from Kathara.manager.Kathara import Kathara
from gi.repository import  Gtk, Gio
from UI.Terminal import Terminal
from Data.Container import Container

class GUIManager:
    def __init__(self):
        self.dialog = Gtk.FileDialog()
        self.dialog.set_title("Select a lab directory")
        self.subscribers = {
            "wiped":[],
            "lab_started":[],
            "reload":[],
            "set_terminal":[],
            "connect_container":[]
        }

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "instance"):
            cls.instance = cls()
        return cls.instance

    def subscribe(self, event, function):
        self.subscribers[event].append(function)

    def notify_subscribers(self,event,*args):
        for subscriber in self.subscribers[event]:
            subscriber(*args)

    def terminal_callback(self,term,status,event):
            self.notify_subscribers(event)

    def select_lab(self):
        self.dialog.select_folder(callback=self.start_lab)

    def start_lab(self,dialog, response_id):
        lab = dialog.select_folder_finish(response_id).get_path()
        self.dialog.set_initial_folder(Gio.File.new_for_path(lab))

        term = Terminal()
        term.connect("child_exited", self.terminal_callback, "lab_started")
        self.notify_subscribers("set_terminal", term)
        term.run(["python", "-m", "kathara", "lrestart","--noterminals", "-d", lab])

    def wipe_all(self):
        term = Terminal()
        term.connect("child_exited", self.on_wipe_finished)
        self.notify_subscribers("set_terminal", term)
        term.run(["sh","-c","python -m kathara wipe && echo 'All Kathara labs have been wiped'"])

    def on_wipe_finished(self,term,status):
        self.notify_subscribers("wiped")
        self.reload()

    def reload(self):
        containers = Kathara.get_instance().get_machines_api_objects()
        containers = [Container(c.labels["name"],c.labels["lab_hash"],c.status) for c in containers]
        self.notify_subscribers("reload", containers)

    def connect_container(self,container):
        self.notify_subscribers("connect_container", container)
