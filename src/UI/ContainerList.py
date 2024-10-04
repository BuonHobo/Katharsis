from gi.repository import Gtk, Adw

from Data.Container import Container
from Messaging.Broker import Broker
from Messaging.Events import ContainersUpdate, \
    LabStartFinish, LabStartBegin, ContainerAdded
from UI.ContainerRow import ContainerRow


class ContainerList(Gtk.ScrolledWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         margin_bottom=10,
                         margin_start=10,
                         margin_end=10,
                         vexpand=True
                         )
        self.status_page = Adw.StatusPage(
            icon_name="dialog-information-symbolic",
            title="No running devices",
            description="Start a lab or reload to see your devices",
        )
        self.rows = Adw.PreferencesGroup()
        self.set_child(self.status_page)
        self.container_rows: dict[Container, ContainerRow] = {}
        self.containers: set[Container] = set()

        Broker.subscribe(ContainersUpdate, self.on_containers_update)
        Broker.subscribe(LabStartBegin, self.disable_entries)
        Broker.subscribe(LabStartFinish, self.enable_entries)
        Broker.subscribe(ContainerAdded, self.on_container_attach)

    def disable_entries(self, _):
        for row in self.container_rows.values():
            row.set_sensitive(False)

    def on_container_attach(self, event: ContainerAdded):
        self.container_rows[event.container].on_attach()

    def enable_entries(self, _):
        for row in self.container_rows.values():
            row.set_sensitive(True)

    def build_row(self, container: Container):
        row = ContainerRow(container)
        return row

    def add_container(self, container: Container):
        row = self.build_row(container)
        self.container_rows[container] = row
        self.rows.add(row)

    def on_containers_update(self, event: ContainersUpdate):
        new_containers = set(event.containers)
        added = new_containers - self.containers
        removed = self.containers - new_containers
        self.containers = new_containers
        for container in added:
            self.add_container(container)
        for container in removed:
            self.remove_container(container)
        if len(self.containers) == 0:
            self.set_child(self.status_page)
        else:
            self.set_child(self.rows)

    def remove_container(self, container: Container):
        row = self.container_rows.pop(container)
        self.rows.remove(row)
