from gi.repository import Adw
from Logic.GUIManager import GUIManager

class MainButtons(Adw.PreferencesGroup):
    def __init__(self):
        super().__init__()
        self.set_margin_bottom(20)
        self.set_margin_end(20)
        self.set_margin_start(20)
        self.add(self.get_button("media-playback-start-symbolic", "Start lab", self.on_start_lab_button_clicked))
        self.add(self.get_button("edit-delete-symbolic", "Wipe", self.on_wipe_lab_button_clicked))
        self.add(self.get_button("view-refresh-symbolic", "Reload", self.on_reload_button_clicked))


    def get_button(self, icon_name, label, callback):
        btn = Adw.ButtonRow()

        btn.set_start_icon_name(icon_name)
        btn.set_title(label)
        btn.set_size_request(0, 50)
        btn.connect("activated", callback)

        return btn

    def on_wipe_lab_button_clicked(self, btn):
        GUIManager.get_instance().wipe_all()

    def on_start_lab_button_clicked(self, btn):
        GUIManager.get_instance().select_lab()

    def on_reload_button_clicked(self, btn):
        GUIManager.get_instance().reload()
