from Data.Container import Container
from Messaging.Broker import Broker
from Messaging.Events import ContainerDisconnected
from UI.Terminal import Terminal


class TerminalManager:
    connect_script = """
from Kathara.manager.Kathara import Kathara
print("Connecting to", '{container.name}' + '...')
Kathara.get_instance().connect_tty(machine_name='{container.name}', lab_hash='{container.lab_hash}')
"""
    __empty = Terminal()
    __shell = None

    def __init__(self):
        self.container_terminals: dict[Container, Terminal] = {}

    def empty(self):
        self.__empty.reset(True, True)
        return self.__empty

    def shell(self):
        if self.__shell is None:
            self.__shell = Terminal()
            self.__shell.run(["bash", "-c", """kathara() { python -m kathara "$@"; } ; export -f kathara ; bash"""])
        return self.__shell

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
            term.unparent()
