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

    def add_person(name, birth_date=None, death_date=None):
        """Add new person"""
        if name in people_data:
            print(f"Person with name {name} already created.")
            return
        people_data[name] = {
            "name": name,
            "birth_date": birth_date,
            "death_date": death_date,
            "parents": [],
            "children": [],
            "siblings": [],
            "spouse": None
        }

    def add_relationship(person_name, relation, relative_name):
        """Function to connect people"""
        if person_name not in people_data or relative_name not in people_data:
            print("Один из указанных людей не найден в базе данных.")
            return
        if relation == "parent":
            people_data[person_name]["parents"].append(relative_name)
            people_data[relative_name]["children"].append(person_name)
        elif relation == "child":
            people_data[person_name]["children"].append(relative_name)
            people_data[relative_name]["parents"].append(person_name)
        elif relation == "sibling":
            people_data[person_name]["siblings"].append(relative_name)
            people_data[relative_name]["siblings"].append(person_name)
        elif relation == "spouse":
            people_data[person_name]["spouse"] = relative_name
            people_data[relative_name]["spouse"] = person_name
        else:
            print("Неизвестный тип связи.")
