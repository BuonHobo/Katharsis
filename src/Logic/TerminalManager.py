from Data.Container import Container
from UI.Terminal import Terminal

from Messaging.Broker import Broker

from Messaging.Events import ContainerDisconnected


class TerminalManager:
    connect_script = """
from Kathara.manager.Kathara import Kathara
print("Connecting to", '{container.name}' + '...')
Kathara.get_instance().connect_tty(machine_name='{container.name}', lab_hash='{container.lab_hash}')
"""
    __empty = Terminal()

    def __init__(self):
        self.container_terminals: dict[Container, Terminal] = {}

    def empty(self):
        self.__empty.reset(True, True)
        return self.__empty

    def get_terminal(self, container: Container):
        if container in self.container_terminals:
            return self.container_terminals[container]

        terminal = Terminal()
        terminal.run(
            [
                "python",
                "-c",
                self.connect_script.format(container=container)
            ])
        terminal.connect("child_exited", self.on_terminal_exited, container)

        self.container_terminals[container] = terminal
        return terminal

    def on_terminal_exited(self, term: Terminal, status: int, container: Container):
        Broker.notify(ContainerDisconnected(container))
        term = self.container_terminals.pop(container)
        if p := term.get_parent():
            p.set_content(None)
