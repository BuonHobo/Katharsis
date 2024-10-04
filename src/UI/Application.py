from Kathara.manager.Kathara import Kathara
from gi.repository import Adw, Gtk, Gio

from Data.Container import Container
from Logic.TerminalManager import TerminalManager
from Messaging.Broker import Broker
from Messaging.Events import ReloadBegin, ContainersUpdate, ContainerDetach, \
    ContainerConnect, SetTerminal, LabSelect, WipeBegin, WipeFinish, LabStartFinish, LabStartBegin, OpenTerminal, \
    ContainerFocused, ContainerAttach
from UI.MainWindow import MainWindow
from UI.TerminalWindow import TerminalWindow


class Application(Adw.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        self.connect("activate", self.on_activate)

        self.set_accels_for_action('win.copy', ['<Ctrl><Shift>c'])
        self.set_accels_for_action('win.paste', ['<Ctrl><Shift>v'])

        self.terminal_manager: TerminalManager = TerminalManager()

        self.dialog = Gtk.FileDialog()
        self.dialog.set_title("Select a lab directory")

        Broker.subscribe(ReloadBegin, self.on_reload_begin)
        Broker.subscribe(ContainerDetach, self.on_container_detach)
        Broker.subscribe(ContainerConnect, self.on_container_connect)

        Broker.subscribe(LabSelect, self.select_lab)
        Broker.subscribe(WipeBegin, self.on_wipe)
        Broker.subscribe(OpenTerminal, self.on_open_terminal)

        Broker.subscribe(ContainerFocused, self.on_container_focused)
        Broker.subscribe(ContainerAttach, self.on_container_attach)

    def on_container_attach(self, event: ContainerAttach):
        term = self.terminal_manager.get_terminal(event.container)
        term.get_root().close()

    def on_container_focused(self, e: ContainerFocused):
        self.terminal_manager.get_terminal(e.container).get_root().present()

    def on_open_terminal(self, _):
        term = self.terminal_manager.shell()
        Broker.notify(SetTerminal(term))

    def select_lab(self, _):
        self.dialog.select_folder(callback=self.on_lab_start)

    def on_lab_start(self, dialog: Gtk.FileDialog, response_id: Gio.AsyncResult):
        lab = dialog.select_folder_finish(response_id).get_path()
        Broker.notify(LabStartBegin())
        self.dialog.set_initial_folder(Gio.File.new_for_path(lab))

        term = self.terminal_manager.empty()
        term.connect("child_exited", lambda t, s: Broker.notify(ReloadBegin()) or Broker.notify(LabStartFinish()))
        term.run(["python", "-m", "kathara", "lrestart", "--noterminals", "-d", lab])
        Broker.notify(SetTerminal(term))

    def on_wipe(self, _):
        term = self.terminal_manager.empty()
        term.connect("child_exited", lambda t, s: Broker.notify(ReloadBegin()) or Broker.notify(WipeFinish()))
        term.run([
            "python", "-m", "kathara", "wipe",
        ])
        Broker.notify(SetTerminal(term))

    def on_activate(self, _):
        MainWindow(application=self).present()
        Broker.notify(ReloadBegin())

    def on_reload_begin(self, event):
        containers = Kathara.get_instance().get_machines_api_objects()
        containers = [Container(c.labels['name'], c.labels['lab_hash']) for c in containers if c.status == 'running']
        Broker.notify(ContainersUpdate(containers))

    def on_container_detach(self, event: ContainerDetach):
        term = self.terminal_manager.get_terminal(event.container)
        if p := term.get_parent():
            p.set_content(None)
        window = TerminalWindow(term, container=event.container)
        self.add_window(window)
        window.present()

    def on_container_connect(self, event: ContainerConnect):
        event = SetTerminal(self.terminal_manager.get_terminal(event.container))
        Broker.notify(event)
