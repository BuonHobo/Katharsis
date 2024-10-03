import Kathara.manager.Kathara
from Logic.GUIManager import GUIManager
from UI.Terminal import Terminal


class TerminalManager:

    instance = None

    def __init__(self):
        self.terminals: dict[tuple[str,str], Terminal] = {}
        if TerminalManager.instance is not None:
            raise Exception("This class is a singleton!")
        TerminalManager.instance = self

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            return TerminalManager()
        return cls.instance

    def get_terminal(self, container: tuple[str,str]):
        print(self.terminals)
        if container in self.terminals:
            print("returned terminal")
            return self.terminals[container]

        terminal = Terminal()
        terminal.run(
            [
                "python",
                "-c",
                f"""
from Kathara.manager.Kathara import Kathara
print("Connecting to", '{container[0]}' + '...')
Kathara.get_instance().connect_tty(machine_name='{container[0]}', lab_hash='{container[1]}')
""",
            ],
        )
        terminal.connect("child_exited",
                         lambda term, status: GUIManager.get_instance().terminal_exited(term, container))
        self.terminals[container] = terminal
        return terminal

    def remove_terminal(self, container: tuple[str,str]):
        if container in self.terminals:
            t = self.terminals.pop(container)
            print("popped", t)