class Container:
    def __init__(self, name: str, lab_hash: str, status: str):
        self.name = name
        self.lab_hash = lab_hash
        self.status = status
        self.detached = False

    def __hash__(self):
        return hash((self.name, self.lab_hash))

    def __eq__(self, other: object):
        return (
                isinstance(other, Container)
                and self.name == other.name
                and self.lab_hash == other.lab_hash
        )
