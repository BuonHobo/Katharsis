class Container:
    def __init__(self, name:str, lab_hash:str,status):
        self.name = name
        self.lab_hash = lab_hash
        self.status=status

    def __hash__(self):
        return hash((self.name,self.lab_hash))

    def __eq__(self, other):
        return self.name == other.name and self.lab_hash == other.lab_hash
