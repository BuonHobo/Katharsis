from __future__ import annotations

from typing import Optional

from gi.repository import Vte, GLib


class Terminal(Vte.Terminal):
    focused: Terminal = None

    def __init__(self):
        super().__init__(margin_top=5, margin_bottom=20, margin_start=20, margin_end=20, bold_is_bright=True)
        self.set_clear_background(False)
        if self.focused is None:
            Terminal.focused = self
        self.connect("notify::has-focus", self.on_focus_changed)

    def on_focus_changed(self, widget: Terminal, v):
        if widget.has_focus():
            Terminal.focused = widget
            print(str(Terminal.focused), "is focused")

    @classmethod
    def on_copy(cls, a, b):
        print("a")
        Terminal.focused.copy_clipboard_format(Vte.Format.TEXT)

    @classmethod
    def on_paste(cls, a, b):
        print("a")

        Terminal.focused.paste_clipboard()

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
