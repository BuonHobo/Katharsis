from typing import Optional

from gi.repository import Vte, GLib


class Terminal(Vte.Terminal):
    def __init__(self):
        super().__init__(margin_top=5, margin_bottom=20, margin_start=30, margin_end=20, bold_is_bright=True)
        self.set_clear_background(False)

    def run(self, command: list[str], working_dir: Optional[str] = None):
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
        )
