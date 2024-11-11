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

    def add_child(self, child):
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)

    def add_sibling(self, sibling):
        if sibling not in self.siblings:
            self.siblings.append(sibling)
            sibling.siblings.append(self)

    def set_spouse(self, spouse):
        self.spouse = spouse
        spouse.spouse = self

    def get_immediate_family(self):
        return {
            "parents": self.parents,
            "siblings": self.siblings,
            "spouse": self.spouse,
            "children": self.children
        }