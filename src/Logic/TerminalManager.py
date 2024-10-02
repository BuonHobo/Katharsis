from Data.Container import Container
from Logic.GUIManager import GUIManager
from UI.Terminal import Terminal


class TerminalManager:
    def __init__(self):
        self.terminals: dict[Container, Terminal] = {}
        GUIManager.get_instance().subscribe("wiped", self.remove_all_terminals)

    def get_terminal(self, container: Container):
        if container in self.terminals:
            return self.terminals[container]

        terminal = Terminal()
        terminal.run(
            [
                "python",
                "-c",
                f"""
from Kathara.manager.Kathara import Kathara
print("Connecting to", '{container.name}' + '...')
Kathara.get_instance().connect_tty(machine_name='{container.name}', lab_hash='{container.lab_hash}')
""",
            ],
        )
        terminal.connect("child_exited",
                         lambda term, status: GUIManager.get_instance().terminal_exited(term, container))
        self.terminals[container] = terminal
        return terminal

    def remove_terminal(self, container: Container):
        if container in self.terminals:
            self.terminals.pop(container)

    def remove_all_terminals(self):
        self.terminals.clear()
