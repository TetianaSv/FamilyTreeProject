from tkinter import Tk, Label, Entry, Button, Text, END
from data import people_data

class Person:

    def __init__(self, name, birth_date=None, death_date=None, parentF=None, parentM=None, spouse=None):

        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date
        self.parentF = parentF
        self.parentM = parentM
        self.spouse = spouse

    def get_spouse(self):
        return self.spouse if self.spouse else 'No spouse'

    def get_parents(self):

        return [self.parentF, self.parentM]

    def get_grandparents(self):

        grandparents = []

        if self.parentF and self.parentF in people_data:

            grandparents.extend(people_data[self.parentF].get("parentF", []))
            grandparents.extend(people_data[self.parentF].get("parentM", []))

        if self.parentM and self.parentM in people_data:

            grandparents.extend(people_data[self.parentM].get("parentF", []))
            grandparents.extend(people_data[self.parentM].get("parentM", []))

        return grandparents

    def get_grandchildren(self):
        grandchildren = []
        # Получаем всех детей
        children = self.get_children()  # Метод для поиска детей нужно добавить, если его еще нет
        for child_name in children:
            child_data = people_data.get(child_name)
            if child_data:
                # Ищем детей у каждого ребенка (т.е. внуков)
                child_person = Person(
                    name=child_data["name"],
                    birth_date=child_data["birth_date"],
                    death_date=child_data["death_date"],
                    parentF=child_data["parentF"][0] if child_data["parentF"] else None,
                    parentM=child_data["parentM"][0] if child_data["parentM"] else None,
                )
                grandchildren.extend(child_person.get_children())
        return grandchildren

    def get_children(self):
        # Метод для нахождения детей текущего человека
        children = []
        for person_name, details in people_data.items():
            if (details.get("parentF") and self.name in details["parentF"]) or \
                    (details.get("parentM") and self.name in details["parentM"]):
                children.append(person_name)
        return children

    def get_siblings(self):
        siblings = []
        for person_name, details in people_data.items():
            # We are looking for siblings who have the same parents and who are not the person himself
            if details["parentF"] == self.parentF and details["parentM"] == self.parentM and person_name != self.name:
                siblings.append(person_name)
        return siblings

    def get_cousins(self):
        cousins = []
        # Получаем родителей текущего человека
        parents = self.get_parents()
        for parent_name in parents:
            if parent_name and parent_name in people_data:
                parent_data = people_data[parent_name]
                parent = Person(
                    name=parent_data["name"],
                    birth_date=parent_data.get("birth_date"),
                    death_date=parent_data.get("death_date"),
                    parentF=parent_data.get("parentF")[0] if parent_data.get("parentF") else None,
                    parentM=parent_data.get("parentM")[0] if parent_data.get("parentM") else None
                )
                # Находим братьев и сестер родителя
                siblings = parent.get_siblings()
                for sibling_name in siblings:
                    # Получаем детей каждого из братьев и сестер (двоюродные братья и сестры)
                    if sibling_name in people_data:
                        sibling_data = people_data[sibling_name]
                        children = sibling_data.get("children", [])
                        cousins.extend(children)
        return cousins

# Task Fa1 and F1b

    def get_immediate_family(self):

        parents = self.get_parents()
        siblings = self.get_siblings()
        spouse = self.get_spouse()
        children = self.get_children()  # Предполагаем, что эта функция возвращает список детей

        return {
            "parents": parents,
            "siblings": siblings,
            "spouse": spouse,
            "children": children
        }

    def get_extended_family(self):
        extended_family = []
        immediate_family = {
            "parents": self.get_parents(),
            "siblings": self.get_siblings(),
            "spouse": [self.get_spouse()]  # Убедимся, что spouse всегда список
        }
        # Добавляем родителей, братьев/сестер и супруга в расширенную семью
        for family_group in immediate_family.values():
            if isinstance(family_group, list):
                extended_family.extend(family_group)  # Разворачиваем список
            elif family_group:  # Проверяем, что значение не None
                extended_family.append(family_group)
        # Добавляем теть и дядей (братьев и сестер родителей)
        for parent in self.get_parents():
            if parent and parent in people_data:
                parent_object = Person(
                    name=parent,
                    birth_date=people_data[parent]["birth_date"],
                    death_date=people_data[parent]["death_date"],
                    parentF=people_data[parent]["parentF"][0] if people_data[parent]["parentF"] else None,
                    parentM=people_data[parent]["parentM"][0] if people_data[parent]["parentM"] else None,
                    spouse=people_data[parent]["spouse"] if "spouse" in people_data[parent] else None
                )
                aunts_uncles = parent_object.get_siblings()
                extended_family.extend(aunts_uncles)
        # Добавляем кузенов
        cousins = self.get_cousins()
        extended_family.extend(cousins)
        # Фильтруем только живых родственников
        extended_family_alive = [
            relative for relative in extended_family
            if isinstance(relative, str) and relative in people_data and not people_data[relative].get("death_date")
        ]
        return extended_family_alive

# Function for searching of relatives
def search_immediate_family():

    name = entry.get()

    if name in people_data:

        data = people_data[name]

        person = Person(

            name=data["name"],

            birth_date=data["birth_date"],

            death_date=data["death_date"],

            parentF=data["parentF"][0] if data["parentF"] else None,

            parentM=data["parentM"][0] if data["parentM"] else None,

            spouse=data["spouse"] if "spouse" in data else None

        )

        immediate_family = person.get_immediate_family()

        result_text.delete(1.0, END)

        result_text.insert(END, f"Immediate family of {name}: {immediate_family}\n")

    else:

        result_text.delete(1.0, END)

        result_text.insert(END, "Person not found in the database.\n")

def search_extended_family():

    name = entry.get()

    if name in people_data:

        data = people_data[name]

        person = Person(

            name=data["name"],

            birth_date=data["birth_date"],

            death_date=data["death_date"],

            parentF=data["parentF"][0] if data["parentF"] else None,

            parentM=data["parentM"][0] if data["parentM"] else None,

            spouse=data["spouse"] if "spouse" in data else None

        )

        extended_family = person.get_extended_family()

        result_text.delete(1.0, END)

        result_text.insert(END, f"Extended family of {name} (alive only): {extended_family}\n")

    else:

        result_text.delete(1.0, END)

        result_text.insert(END, "Person not found in the database.\n")


# Set up of Tkinder window

root = Tk()
root.title("Search relatives")
root.geometry("500x400")
Label(root, text="Enter a name:").pack(pady=5)
entry = Entry(root, width=40)
entry.pack(pady=5)
# Добавляем кнопки с отдельными вызовами .pack()
Button(root, text="Search Immediate Family", command=search_immediate_family).pack(pady=5)
Button(root, text="Search Extended Family", command=search_extended_family).pack(pady=5)
# Создаем текстовое поле для отображения результатов
result_text = Text(root, height=10, width=50)
result_text.pack(pady=5)
# Запускаем главное окно Tkinter
root.mainloop()