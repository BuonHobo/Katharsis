import Data.Container


class Event: pass


class MainButtonEvent(Event): pass


class LabEvent(MainButtonEvent): pass


class LabSelect(LabEvent): pass


class LabStartFinish(LabEvent): pass


class WipeEvent(MainButtonEvent): pass


class WipeBegin(WipeEvent): pass


class WipeFinish(WipeEvent): pass


class ReloadEvent(MainButtonEvent): pass


class ReloadBegin(ReloadEvent): pass


class ReloadFinish(ReloadEvent): pass


class ContainerEvent(Event): pass


class ContainersUpdate(ReloadFinish):
    def __init__(self, containers: list[Data.Container.Container]):
        self.containers = containers


class ContainerDeleted(ContainerEvent):
    def __init__(self, container: Data.Container.Container):
        self.container = container


class ContainerAdded(ContainerEvent):
    def __init__(self, container: Data.Container.Container):
        self.container = container


class ContainerConnect(ContainerEvent):
    def __init__(self, container: Data.Container.Container):
        self.container = container


class ContainerDetach(ContainerEvent):
    def __init__(self, container: Data.Container.Container):
        self.container = container


class ContainerAttach(ContainerEvent):
    def __init__(self, container: Data.Container.Container):
        self.container = container


class TerminalEvent(Event): pass


class TerminalCopyEvent(TerminalEvent): pass


class TerminalPasteEvent(TerminalEvent): pass


class SetTerminal(TerminalEvent):
    def __init__(self, terminal):
        self.terminal = terminal


class LabStartBegin(LabEvent): pass

class ContainerDisconnected(ContainerEvent):
    def __init__(self, container: Data.Container.Container):
        self.container = container

class Shutdown(Event):
    pass