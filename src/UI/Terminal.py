from gi.repository import Vte, GLib


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
