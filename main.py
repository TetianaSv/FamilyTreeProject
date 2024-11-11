class Person:
    def __init__(self, name, birth_date=None, death_date=None,):
        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date
        self.parents = []
        self.children = []
        self.spouse = None

    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.append(parent)
            parent.children.append(self)
