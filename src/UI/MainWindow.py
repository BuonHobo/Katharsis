from gi.repository import Adw, Gtk

from Messaging.Broker import Broker
from Messaging.Events import LabSelect, WipeBegin, ReloadBegin, ContainerConnect, SetTerminal, ContainerDetach, \
    WipeFinish, LabStartFinish, ContainerDeleted
from UI.ApplicationWindow import ApplicationWindow
from UI.ContainerList import ContainerList
from UI.InitialTerminal import InitialTerminal
from UI.Terminal import Terminal


class MainWindow(ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Katharsis")
        self.set_content(Adw.OverlaySplitView(sidebar=self.get_sidebar(), content=self.get_panel()))

        self.cp = self.lookup_action('copy').connect('activate', self.on_copy)
        self.pst = self.lookup_action('paste').connect('activate', self.on_paste)

        self.terminal = None
        self.switch_terminal(InitialTerminal())

        self.cp = 1
        self.pst = 1

        Broker.subscribe(SetTerminal, self.set_terminal)

    def on_copy(self, a, b):
        self.terminal.on_copy()

    def on_paste(self, a, b):
        self.terminal.on_paste()

    def get_sidebar(self):
        sb = Adw.ToolbarView()
        sb.add_top_bar(Adw.HeaderBar(show_title=True))
        sb.add_bottom_bar(self.get_main_buttons())
        sb.set_content(ContainerList())
        return sb

    def get_main_buttons(self):
        mb = Gtk.Box(margin_end=10,
                     margin_start=10,
                     margin_top=10,
                     margin_bottom=10,
                     spacing=10)
        start = Gtk.Button(
            icon_name="media-playback-start-symbolic",
            tooltip_text="Start or restart a lab",
            hexpand=True
        )
        start.connect("clicked", lambda _: Broker.notify(LabSelect()))
        mb.append(start)

        wipe = Gtk.Button(
            icon_name="user-trash-symbolic",
            tooltip_text="Wipe all labs",
            hexpand=True
        )
        wipe.connect("clicked", lambda _: Broker.notify(WipeBegin()))
        mb.append(wipe)

        reload = Gtk.Button(
            icon_name="view-refresh-symbolic",
            tooltip_text="Reload running containers",
            hexpand=True
        )
        reload.connect("clicked", lambda _: Broker.notify(ReloadBegin()))
        mb.append(reload)

        return mb

    def get_topbar(self):
        wt = Adw.WindowTitle(title="")

        Broker.subscribe(ContainerConnect, lambda e: wt.set_title(e.container.name))
        Broker.subscribe(WipeBegin, lambda _: wt.set_title("Wiping lab..."))
        Broker.subscribe(LabSelect, lambda _: wt.set_title("(Re)starting lab..."))
        Broker.subscribe(ContainerDetach,
                         lambda e: wt.set_title("" if wt.get_title() == e.container.name else wt.get_title()))
        Broker.subscribe(ContainerDeleted,
                         lambda e: wt.set_title("" if wt.get_title() == e.container.name else wt.get_title()))
        Broker.subscribe(WipeFinish, lambda _: wt.set_title(""))
        Broker.subscribe(LabStartFinish, lambda _: wt.set_title(""))

        return Adw.HeaderBar(show_title=True, title_widget=wt)

    def get_panel(self):
        ct = Adw.ToolbarView()
        ct.add_top_bar(self.get_topbar())
        return ct

    def set_terminal(self, event: SetTerminal):
        self.switch_terminal(event.terminal)

    def switch_terminal(self, terminal: Terminal):
        if terminal == self.terminal:
            return
        self.terminal = terminal
        self.get_content().get_content().set_content(self.terminal)
        self.terminal.grab_focus()
