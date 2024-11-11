from data import people_data

class Person:
    def __init__(self, name, parentF, parentM, birth_date=None, death_date=None):
        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date
        self.parentF = parentF
        self.parentM = parentM
        self.parents = []
        self.children = []
        self.spouse = None


def get_parents(self):
    """Возвращает список родителей."""
    parents = []
    if self.parentF:
        parents.append(self.parentF.name)
    if self.parentM:
        parents.append(self.parentM.name)
    return parents or "Родители неизвестны"


def get_grandparents(self):
    """Возвращает список бабушек и дедушек."""
    grandparents = []
    if self.parentF:
        if self.parentF.parentF:
            grandparents.append(self.parentF.parentF.name)
        if self.parentF.parentM:
            grandparents.append(self.parentF.parentM.name)
    if self.parentM:
        if self.parentM.parentF:
            grandparents.append(self.parentM.parentF.name)
        if self.parentM.parentM:
            grandparents.append(self.parentM.parentM.name)
    return grandparents or "Бабушки и дедушки неизвестны"