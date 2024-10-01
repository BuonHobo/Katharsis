from gi.repository import Gtk, Adw
from Data.Container import Container
from UI.ContainerRow import ContainerRow
from Logic.GUIManager import GUIManager

class ContainerList(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.set_margin_bottom(20)
        self.set_vexpand(True)
        self.containers:dict[Container,ContainerRow]={}
        self.containers_set = set()
        self.containers_rows = self.get_containers_rows()
        self.set_child(self.containers_rows)
        GUIManager.get_instance().subscribe("reload",self.update_containers)

    def get_containers_rows(self):
        group = Adw.PreferencesGroup()
        group.set_title("Reload to get containers")
        group.set_margin_end(20)
        group.set_margin_start(20)
        return group

    def add_container(self, container):
        row = self.get_row(container)
        self.containers[container] = row
        self.containers_set.add(container)
        self.containers_rows.add(row)
        self.containers_rows.set_title("")

    def get_row(self, container):
        row = Adw.ButtonRow()
        row.set_size_request(0, 50)
        row.connect("activated", lambda btn :GUIManager.get_instance().connect_container(container))
        row.set_title(container.name)
        row.set_start_icon_name("utilities-terminal-symbolic")
        row.set_sensitive(container.status == "running")
        return row

    def remove_container(self, container):
        if len(self.containers)==0:
            self.containers_rows.set_title("Reload to get containers")
        row = self.containers.pop(container)
        self.containers_set.remove(container)
        self.containers_rows.remove(row)

    def update_containers(self, containers):
        new_containers_set = set(containers)
        print(self.containers_set, new_containers_set)
        for container in new_containers_set - self.containers_set:
            print("Adding container", container.name)
            self.add_container(container)
        for container in self.containers_set - new_containers_set:
            print("Removing container", container.name)

            self.remove_container(container)
        self.containers_set = new_containers_set
