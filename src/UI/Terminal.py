from gi.repository import Vte, GLib, Gtk, Gio


class Terminal(Vte.Terminal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         allow_hyperlink=True,
                         bold_is_bright=True,
                         margin_top=10,
                         margin_bottom=10,
                         margin_end=10,
                         margin_start=10)
        self.set_clear_background(False)

        m = Gio.Menu()
        m.append("Copy", "win.copy")
        m.append("Paste", "win.paste")

        self.set_context_menu(Gtk.PopoverMenu.new_from_model(m))

    def on_copy(self):
        self.copy_clipboard_format(Vte.Format.TEXT)

    def on_paste(self):
        self.paste_clipboard()

    def run(self, command: list[str]):
        self.spawn_async(
            Vte.PtyFlags.DEFAULT,
            None,
            command,
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
        )
