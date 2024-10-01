from UI.Terminal import Terminal
from Data.Container import Container

class TerminalManager:
    def __init__(self):
        self.terminals:dict[Container,Terminal]={}

    def get_terminal(self, container:Container):
        if container in self.terminals:
            return self.terminals[container]

        terminal = Terminal()
        terminal.run(["python","src/connect.py", container.name, container.lab_hash],)
        self.terminals[container] = terminal
        return terminal

    def remove_terminal(self, container:Container):
        if container in self.terminals:
            self.terminals.pop(container)

    def remove_all_terminals(self):
        self.terminals.clear()
