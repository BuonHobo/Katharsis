from gi.repository import Adw, Gtk

from Data.Container import Container
from Messaging.Broker import Broker
from Messaging.Events import ContainerConnect, ContainerDetach, ContainerFocused, ContainerAttach


class ContainerRow(Adw.ActionRow):

    def __init__(self, container: Container, *args, **kwargs):
        super().__init__(*args, **kwargs, title=container.name, activatable=True,
                         tooltip_text=f"Connect to {container.name}")

        self.detached = False
        self.container = container
        self.add_prefix(Gtk.Image(icon_name="network-server-symbolic", pixel_size=15))
        self.connect("activated", self.on_activate)
        self.btn = Gtk.Button(
            icon_name="window-new-symbolic",
            has_frame=False,
            margin_top=5,
            margin_bottom=5,
            tooltip_text=f"Connect to {container.name} in a different window",
        )
        self.btn.connect("clicked", lambda _: self.on_button_clicked())
        self.add_suffix(self.btn)

    def on_button_clicked(self):
        if not self.detached:
            self.set_button_attach()
            Broker.notify(ContainerDetach(self.container))
        else:
            self.set_button_detach()
            Broker.notify(ContainerAttach(self.container))

    def set_button_detach(self):
        self.detached = False
        self.btn.set_icon_name("window-new-symbolic")
        self.btn.set_tooltip_text(f"Connect to {self.container.name} in a different window")

    def set_button_attach(self):
        self.detached = True
        self.btn.set_icon_name("edit-undo-symbolic")
        self.btn.set_tooltip_text(f"Reattach the window associated with {self.container.name}")

    def on_activate(self, _):
        if self.detached:
            Broker.notify(ContainerFocused(self.container))
        else:
            Broker.notify(ContainerConnect(self.container))

    def on_attach(self):
        self.set_button_detach()
