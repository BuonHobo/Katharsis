from gi.repository import Vte, GLib


class Terminal(Vte.Terminal):
    def __init__(self):
        super().__init__()

        self.set_clear_background(False)
        self.set_margin_bottom(20)
        self.set_margin_end(20)
        self.set_margin_start(20)
        self.set_bold_is_bright(True)

    def run(self, command:list[str],working_dir=None):
        self.spawn_async(
            Vte.PtyFlags.DEFAULT,
            working_dir,
            command,
            None,
            GLib.SpawnFlags.DEFAULT,
            None,
            None,
            -1,
            None,
            None,
        )
