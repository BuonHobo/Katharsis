#!/usr/bin/python

import sys

import gi
from Kathara.manager.Kathara import Kathara

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version("Vte", "3.91")
from gi.repository import Adw, GLib, Gtk, Vte


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_titlebar(Gtk.Box())
        self.set_title("Kathara GUI")

        self.containers = []
        self.terminals: dict[tuple[str, str], Vte.Terminal] = {}
        self.scrolled_window = self.get_scrolled_window()
        self.terminal_window = self.get_content()

        nav = Adw.OverlaySplitView()
        nav.set_sidebar(self.get_sidebar())
        nav.set_content(self.terminal_window)

        self.set_child(nav)

    def get_content(self):
        content = Adw.ToolbarView()
        header = Adw.HeaderBar()
        header.set_show_title(False)
        content.add_top_bar(header)
        content.set_size_request(400, 300)
        content.set_content(self.get_terminal())
        return content

    def get_terminal(self):
        terminal = Vte.Terminal()

        terminal.set_clear_background(False)
        # terminal.set_margin_top(20)
        terminal.set_margin_bottom(20)
        terminal.set_margin_end(20)
        terminal.set_margin_start(20)
        terminal.set_bold_is_bright(True)

        return terminal

    def on_connect_button_clicked(self, button, labels):
        print("Connecting to", labels["name"] + "...")

        if self.terminals.get((labels["name"], labels["lab_hash"])):
            self.terminal_window.set_content(
                self.terminals[(labels["name"], labels["lab_hash"])]
            )
            return

        terminal = self.get_terminal()
        self.terminals[(labels["name"], labels["lab_hash"])] = terminal
        self.terminal_window.set_content(terminal)
        terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            ["python", "/app/bin/connect.py", labels["name"], labels["lab_hash"]],
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None,
        )

    def get_sidebar(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(self.get_top_commands())

        main_box.append(self.scrolled_window)

        content = Adw.ToolbarView()
        header = Adw.HeaderBar()
        content.add_top_bar(header)
        content.set_content(main_box)


        return main_box

    def get_containers_rows(self):
        group = Adw.PreferencesGroup()
        group.set_title("" if len(self.containers) > 0 else "Reload to get containers")
        group.set_margin_end(20)
        group.set_margin_start(20)
        for container in self.containers:
            btn = Adw.ButtonRow()
            content = Adw.ButtonContent()
            content.set_label(container.labels["name"])
            content.set_icon_name("utilities-terminal-symbolic")
            btn.set_child(content)
            btn.set_size_request(0, 50)
            btn.connect("activated", self.on_connect_button_clicked, container.labels)

            if container.status != "running":
                btn.set_sensitive(False)

            group.add(btn)

        return group

    def get_scrolled_window(self):
        window = Gtk.ScrolledWindow()
        window.set_margin_bottom(20)
        window.set_vexpand(True)

        window.set_child(self.get_containers_rows())

        return window

    def get_top_commands(self):
        top_box = Adw.PreferencesGroup()
        top_box.set_margin_top(20)
        top_box.set_margin_bottom(20)
        top_box.set_margin_end(20)
        top_box.set_margin_start(20)

        top_box.add(self.get_start_lab_button())
        top_box.add(self.get_wipe_lab_button())
        top_box.add(self.get_refresh_button())

        return top_box

    def get_start_lab_button(self):
        btn = Adw.ButtonRow()

        content = Adw.ButtonContent()
        content.set_icon_name("media-playback-start-symbolic")
        content.set_label("Start lab")
        btn.set_size_request(0, 50)

        btn.set_child(content)
        btn.connect("activated", self.on_start_lab_button_clicked)

        return btn

    def get_wipe_lab_button(self):
        btn = Adw.ButtonRow()

        content = Adw.ButtonContent()
        content.set_icon_name("edit-delete-symbolic")
        content.set_label("Wipe")
        btn.set_size_request(0, 50)

        btn.set_child(content)
        btn.connect("activated", self.on_wipe_lab_button_clicked)

        return btn

    def get_refresh_button(self):
        btn = Adw.ButtonRow()

        content = Adw.ButtonContent()
        content.set_icon_name("view-refresh-symbolic")
        content.set_label("Reload")
        btn.set_size_request(0, 50)

        btn.set_child(content)
        btn.connect("activated", self.on_reload_button_clicked)

        return btn

    def on_wipe_lab_button_clicked(self, btn):
        print("Wiping lab now")

        self.terminals.clear()
        t = self.get_terminal()
        self.terminal_window.set_content(t)
        t.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            ["python", "-m", "kathara", "wipe", "-f"],
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None,
        )

    def on_folder_selected(self, dialog, response_id):
        lab = dialog.select_folder_finish(response_id).get_path()
        self.terminals.clear()
        t = self.get_terminal()
        self.terminal_window.set_content(t)
        t.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            ["python", "-m", "kathara", "lrestart", "-d", lab],
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None,
        )

    def on_start_lab_button_clicked(self, btn):
        print("Starting lab now")
        open_dialog = Gtk.FileDialog()
        open_dialog.set_title("Open a kathara lab")
        open_dialog.select_folder(self, None, callback=self.on_folder_selected)

    def on_reload_button_clicked(self, btn):
        print("Reloading containers")
        self.containers = list(Kathara.get_instance().get_machines_api_objects())
        self.scrolled_window.set_child(self.get_containers_rows())


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


def main():
    app = MyApp(application_id="io.github.buonhobo.KatharaGUI")
    app.run(sys.argv)


main()
