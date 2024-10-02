from typing import Callable

from gi.repository import Gtk

from Logic.GUIManager import GUIManager


class MainButtons(Gtk.Box):
    def __init__(self):
        super().__init__(margin_end=10, margin_start=10, margin_top=15, margin_bottom=15)
        self.append(
            self.get_button(
                "media-playback-start-symbolic",
                "Start or restart a lab",
                lambda btn: GUIManager.get_instance().select_lab(),
            )
        )
        self.append(
            self.get_button(
                "user-trash-symbolic",
                "Wipe all labs",
                lambda btn: GUIManager.get_instance().wipe_all(),
            )
        )
        self.append(
            self.get_button(
                "view-refresh-symbolic",
                "Reload running containers",
                lambda btn: GUIManager.get_instance().reload(),
            )
        )

    @staticmethod
    def get_button(icon_name: str, label: str, callback: Callable):
        btn = Gtk.Button(icon_name=icon_name, tooltip_text=label, margin_end=5, margin_start=5, height_request=30,
                         hexpand=True)
        btn.connect("clicked", callback)
        return btn
