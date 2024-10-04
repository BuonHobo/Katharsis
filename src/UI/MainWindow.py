from gi.repository import Adw, Gtk

from Messaging.Broker import Broker
from Messaging.Events import ContainerDisconnected, LabStartBegin, ContainerAdded
from Messaging.Events import LabSelect, WipeBegin, ReloadBegin, ContainerConnect, SetTerminal, ContainerDetach, \
    WipeFinish, LabStartFinish, ContainerDeleted, OpenTerminal
from Messaging.Events import Shutdown
from UI.ApplicationWindow import ApplicationWindow
from UI.ContainerList import ContainerList
from UI.InitialTerminal import InitialTerminal
from UI.Terminal import Terminal


class MainWindow(ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title="Katharsis")
        self.set_content(Adw.OverlaySplitView(sidebar=self.get_sidebar(), content=self.get_panel()))

        self.lookup_action('copy').connect('activate', self.on_copy)
        self.lookup_action('paste').connect('activate', self.on_paste)

        self.connect("close-request", lambda _: Broker.notify(Shutdown()))

        self.terminal = None
        self.switch_terminal(InitialTerminal())

        Broker.subscribe(SetTerminal, self.set_terminal)
        Broker.subscribe(ContainerAdded, self.on_added)

    def on_added(self, e: ContainerAdded):
        c = self.get_content().get_content().get_content()
        if (c is None) or (c is not self.terminal):
            Broker.notify(ContainerConnect(e.container))

    def on_copy(self, a, b):
        self.terminal.on_copy()

    def on_paste(self, a, b):
        self.terminal.on_paste()

    def get_sidebar(self):
        sb = Adw.ToolbarView()
        tb = Adw.HeaderBar(show_title=True)
        bt = Gtk.Button(icon_name="utilities-terminal-symbolic",
                        tooltip_text="Open a bash terminal with access to kathara")
        bt.connect("clicked", lambda _: Broker.notify(OpenTerminal()))
        tb.pack_start(bt)
        sb.add_top_bar(tb)
        sb.add_bottom_bar(self.get_main_buttons())
        sb.set_content(ContainerList())
        return sb

    def get_main_buttons(self):
        mb = Gtk.Box(margin_end=10,
                     margin_start=10,
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
        Broker.subscribe(LabStartBegin, lambda _: wt.set_title("(Re)starting lab..."))
        Broker.subscribe(ContainerDetach,
                         lambda e: wt.set_title("" if wt.get_title() == e.container.name else wt.get_title()))
        Broker.subscribe(ContainerDeleted,
                         lambda e: wt.set_title("" if wt.get_title() == e.container.name else wt.get_title()))
        Broker.subscribe(WipeFinish, lambda _: wt.set_title(""))
        Broker.subscribe(LabStartFinish, lambda _: wt.set_title(""))
        Broker.subscribe(ContainerDisconnected,
                         lambda e: wt.set_title("" if wt.get_title() == e.container.name else wt.get_title()))
        Broker.subscribe(OpenTerminal, lambda _: wt.set_title("Integrated shell, good luck"))

        return Adw.HeaderBar(show_title=True, title_widget=wt)

    def get_panel(self):
        ct = Adw.ToolbarView()
        ct.add_top_bar(self.get_topbar())
        return ct

    def set_terminal(self, event: SetTerminal):
        self.switch_terminal(event.terminal)

    def switch_terminal(self, terminal: Terminal):
        if self.get_content().get_content() is terminal.get_parent():
            return
        self.terminal = terminal
        self.get_content().get_content().set_content(self.terminal)
        self.terminal.grab_focus()
