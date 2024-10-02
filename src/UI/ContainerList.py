from gi.repository import Gtk, Adw

from Data.Container import Container
from Logic.GUIManager import GUIManager


class ContainerList(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__(vexpand=True)
        self.containers: dict[Container, Gtk.Button] = {}
        self.status_page = Adw.StatusPage(icon_name="dialog-question", title="No Running Labs",
                                          description="Start a Lab or reload to see your devices")
        self.containers_rows = Adw.PreferencesGroup(margin_end=10, margin_start=10)
        self.set_child(self.status_page)

        GUIManager.get_instance().subscribe("reload", self.update_containers)
        GUIManager.get_instance().subscribe("detach_container", self.on_container_detached)
        GUIManager.get_instance().subscribe("attach_container", self.on_attach_container)

    def get_row2(self, container: Container):
        row = Adw.ActionRow(
            title=container.name,
            activatable=True)
        row.add_prefix(Gtk.Image(icon_name="utilities-terminal-symbolic", pixel_size=20))
        cut = Gtk.Button(icon_name="edit-cut-symbolic", has_frame=False, margin_top=5, margin_bottom=5)
        row.add_suffix(cut)
        row.connect(
            "activated",
            lambda btn: GUIManager.get_instance().connect_container(container),
        )
        cut.connect("clicked", lambda btn: GUIManager.get_instance().detach_container(container))
        return row

    def add_container(self, container: Container):
        if len(self.containers) == 0:
            self.set_child(self.containers_rows)

        row = self.get_row2(container)
        self.containers[container] = row
        self.containers_rows.add(row)

    def remove_container(self, container: Container):
        row = self.containers.pop(container)
        self.containers_rows.remove(row)
        if len(self.containers) == 0:
            self.set_child(self.status_page)

    def update_containers(self, containers: list[Container]):
        new_containers_set = set(containers)
        old_containers_set = self.containers.keys()
        for container in new_containers_set - old_containers_set:
            self.add_container(container)
        for container in old_containers_set - new_containers_set:
            self.remove_container(container)

    def on_container_detached(self, container: Container):
        self.containers[container].set_sensitive(False)

    def on_attach_container(self, container: Container, term):
        self.containers[container].set_sensitive(True)
