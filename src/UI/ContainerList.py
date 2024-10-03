from gi.repository import Gtk, Adw, GLib

from Logic.GUIManager import GUIManager


class ContainerList(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__(vexpand=True)
        self.containers: dict[tuple[str,str], Adw.ActionRow] = {}
        self.status_page = Adw.StatusPage(icon_name="dialog-question", title="No Running Labs",
                                          description="Start a Lab or reload to see your devices")
        self.containers_rows = Adw.PreferencesGroup(margin_end=10, margin_start=10)
        self.set_child(self.status_page)

        GUIManager.get_instance().subscribe("reload", self.update_containers)
        GUIManager.get_instance().subscribe("detach_container", self.on_container_detached)
        GUIManager.get_instance().subscribe("attach_container", self.on_attach_container)

    def get_row2(self, container: tuple[str,str]):
        row = Adw.ActionRow(
            title=container[0],
            activatable=True,tooltip_text=f"Connect to {container[0]}")
        row.add_prefix(Gtk.Image(icon_name="utilities-terminal-symbolic", pixel_size=20))
        cut = Gtk.Button(icon_name="edit-cut-symbolic", has_frame=False, margin_top=5, margin_bottom=5,tooltip_text=f"Connect to {container[0]} in a different window")
        cut.set_action_name("win.detach")
        cut.set_action_target_value(GLib.Variant.new_array(GLib.VariantType.new("s"),
            [
                GLib.Variant.new_string(container[0]),
                GLib.Variant.new_string(container[1]),
            ]
        ))
        row.add_suffix(cut)
        row.connect(
            "activated",
            lambda btn: GUIManager.get_instance().connect_container(container),
        )
        cut.connect("clicked", lambda btn: GUIManager.get_instance().detach_container(container))
        return row

    def add_container(self, container: tuple[str,str]):
        if len(self.containers) == 0:
            self.set_child(self.containers_rows)

        row = self.get_row2(container)
        self.containers[(container[0],container[1])] = row
        self.containers_rows.add(row)

    def remove_container(self, container: tuple[str,str]):
        row = self.containers.pop((container[0],container[1]))
        self.containers_rows.remove(row)
        if len(self.containers) == 0:
            self.set_child(self.status_page)

    def update_containers(self, containers: list[tuple[str,str]]):
        new_containers_set = set(containers)
        old_containers_set = self.containers.keys()
        for container in new_containers_set - old_containers_set:
            self.add_container(container)
        for container in old_containers_set - new_containers_set:
            self.remove_container(container)

    def on_container_detached(self, container: tuple[str,str]):
        self.containers[container].set_sensitive(False)

    def on_attach_container(self, container: tuple[str,str], term):
        self.containers[container].set_sensitive(True)
