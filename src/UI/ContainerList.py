from gi.repository import Gtk, Adw

from Data.Container import Container
from Messaging.Broker import Broker
from Messaging.Events import ContainerConnect, ContainerDetach, ContainerAdded, ContainerDeleted, ContainersUpdate


class ContainerList(Gtk.ScrolledWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         margin_top=10,
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
        self.container_rows: dict[Container, Adw.ActionRow] = {}
        self.containers: set[Container] = set()

        Broker.subscribe(ContainerAdded, self.on_container_added)
        Broker.subscribe(ContainerDeleted, self.on_container_deleted)
        Broker.subscribe(ContainersUpdate, self.on_containers_update)

    def build_row(self, container: Container):
        row = Adw.ActionRow(
            title=container.name,
            activatable=True,
            tooltip_text=f"Connect to {container.name}",
        )

        row.add_prefix(Gtk.Image(icon_name="utilities-terminal-symbolic", pixel_size=20))
        row.connect("activated", self.on_row_activated, container)

        detach = Gtk.Button(
            icon_name="edit-cut-symbolic",
            has_frame=False,
            margin_top=5,
            margin_bottom=5,
            tooltip_text=f"Connect to {container.name} in a different window",
        )
        detach.connect("clicked", self.on_detach, container)
        row.add_suffix(detach)
        self.container_rows[container] = row
        return row

    def on_row_activated(self, row: Adw.ActionRow, container: Container):
        Broker.notify(ContainerConnect(container))

    def on_detach(self, btn: Gtk.Button, container: Container):
        Broker.notify(ContainerDetach(container))

    def on_container_added(self, event: ContainerAdded):
        row = self.build_row(event.container)
        self.rows.add(row)

    def on_containers_update(self, event: ContainersUpdate):
        new_containers = set(event.containers)
        added = new_containers - self.containers
        removed = self.containers - new_containers
        self.containers = new_containers
        for container in added:
            Broker.notify(ContainerAdded(container))
        for container in removed:
            Broker.notify(ContainerDeleted(container))
        if len(self.containers) == 0:
            self.set_child(self.status_page)
        else:
            self.set_child(self.rows)

    def on_container_deleted(self, event: ContainerDeleted):
        row = self.container_rows.pop(event.container)
        self.rows.remove(row)
