  #project completed by Tetiana Svynar 001390358 and Uzbek Imtiaz Cheema 001364457
  #Task F1a and F1b was developed by Tetiana
  #Task F2a and F2b was developed by Cheema
  #Task F3 a and b done together
from tkinter import Tk, Label, Button, Text, StringVar, OptionMenu, END
from data import people_data
from datetime import datetime
from collections import defaultdict

class Person:

    def __init__(self, name, birth_date=None, death_date=None, parentF=None, parentM=None, spouse=None):

        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date
        self.parentF = parentF
        self.parentM = parentM
        self.spouse = spouse

    # method to find spouse
    def get_spouse(self):
        return self.spouse if self.spouse else 'No spouse'

    # TASK F1

    # Task F1a i
    # method to find parents
    def get_parents(self):

        return [self.parentF, self.parentM]

    # method to find children
    def get_children(self):
        # Method to find children of current person
        children = []
        for person_name, details in people_data.items():
            if (details.get("parentF") and self.name in details["parentF"]) or \
                    (details.get("parentM") and self.name in details["parentM"]):
                children.append(person_name)
        return children

    # method to find grandparents
    def get_grandparents(self):

        grandparents = []

        if self.parentF and self.parentF in people_data:

            grandparents.extend(people_data[self.parentF].get("parentF", []))
            grandparents.extend(people_data[self.parentF].get("parentM", []))

        if self.parentM and self.parentM in people_data:

            grandparents.extend(people_data[self.parentM].get("parentF", []))
            grandparents.extend(people_data[self.parentM].get("parentM", []))

        return grandparents

    # Task F1a ii
    # method to find grandchildren
    def get_grandchildren(self):
        grandchildren = []
        # get all children
        children = self.get_children()  # Метод для поиска детей нужно добавить, если его еще нет
        for child_name in children:
            child_data = people_data.get(child_name)
            if child_data:
                # Searching for a children of each child
                child_person = Person(
                    name=child_data["name"],
                    birth_date=child_data["birth_date"],
                    death_date=child_data["death_date"],
                    parentF=child_data["parentF"][0] if child_data["parentF"] else None,
                    parentM=child_data["parentM"][0] if child_data["parentM"] else None,
                )
                grandchildren.extend(child_person.get_children())
        return grandchildren

    # TASK F2
    #Task F2a i
    # method to find siblings
    def get_siblings(self):
        siblings = []
        for person_name, details in people_data.items():
            # We are looking for siblings who have the same parents and who are not the person himself
            if details["parentF"] == self.parentF and details["parentM"] == self.parentM and person_name != self.name:
                siblings.append(person_name)
        return siblings

    # Task F2a ii
    # method to find cousins
    def get_cousins(self):
        cousins = []
        # Get the current person's parents
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
                # Finding the parent's brothers and sisters
                siblings = parent.get_siblings()
                for sibling_name in siblings:
                    # We get the children of each of the brothers and sisters (cousins)                    if sibling_name in people_data:
                        sibling_data = people_data[sibling_name]
                        children = sibling_data.get("children", [])
                        cousins.extend(children)
        return cousins

    # TASK F1b
    # Task F1b i
    def get_immediate_family(self):

        parents = self.get_parents()
        siblings = self.get_siblings()
        spouse = self.get_spouse()
        children = self.get_children()

        return {
            "parents": parents,
            "siblings": siblings,
            "spouse": spouse,
            "children": children
        }

    # Task F1b ii
    def get_extended_family(self):
        extended_family = []
        immediate_family = {
            "parents": self.get_parents(),
            "siblings": self.get_siblings(),
            "spouse": [self.get_spouse()]  # Let's make sure that spouse is always a list
        }
        # Add parents, siblings and spouse to extended family
        for family_group in immediate_family.values():
            if isinstance(family_group, list):
                extended_family.extend(family_group)  # Expand the list
            elif family_group:  # Check that the value is not None
                extended_family.append(family_group)
        # Adding aunts and uncles (parents' brothers and sisters)
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
        # Add cousins
        cousins = self.get_cousins()
        extended_family.extend(cousins)
        # We filter only living relatives
        extended_family_alive = [
            relative for relative in extended_family
            if isinstance(relative, str) and relative in people_data and not people_data[relative].get("death_date")
        ]
        return extended_family_alive

    def get_ancestors(self):
        # Returns all ascending relatives (ancestors)
        ancestors = set()

        def find_ancestors(person):
            if person in people_data:
                parents = (people_data[person].get("parentF") or []) + (people_data[person].get("parentM") or [])
                for parent in parents:
                    if parent not in ancestors:  # Избегаем циклов
                        ancestors.add(parent)
                        find_ancestors(parent)

        find_ancestors(self.name)
        return list(ancestors)

    def get_descendants(self):
        # Returns all descendants of a given item.
        descendants = set()

        def find_descendants(person):
            for potential_descendant, details in people_data.items():
                parents = (details.get("parentF") or []) + (details.get("parentM") or [])
                if person in parents and potential_descendant not in descendants:
                    descendants.add(potential_descendant)
                    find_descendants(potential_descendant)

        find_descendants(self.name)
        return list(descendants)

    def get_branch_birthdays(self):
        # Finds the birthdays of all members of a branch.
        branch = set(self.get_ancestors() + self.get_descendants())
        birthdays = []
        for relative in branch:
            if relative in people_data and people_data[relative].get("birth_date"):
                birthdays.append(f"{relative}: {people_data[relative]['birth_date']}")
        return birthdays

    # Calculate average age at death
    @staticmethod #to define a static method in a class
    def calculate_average_age_at_death():
        total_age = 0
        count = 0
        for person_data in people_data.values():
            if person_data.get("death_date") and person_data.get("birth_date"):
                birth_date = datetime.strptime(person_data["birth_date"], "%Y-%m-%d")
                death_date = datetime.strptime(person_data["death_date"], "%Y-%m-%d")
                total_age += (death_date - birth_date).days / 365.25
                count += 1
        return total_age / count if count > 0 else 0


def show_parents():
    name = selected_name.get()
    if name == "Select a name":
        result_text.delete(1.0, END)
        result_text.insert(END, "Please select a name from the list.\n")
        return

    if name in people_data:
        person_data = people_data[name]
        person = Person(
            name=person_data["name"],
            birth_date=person_data.get("birth_date"),
            death_date=person_data.get("death_date"),
            parentF=person_data.get("parentF")[0] if person_data.get("parentF") else None,
            parentM=person_data.get("parentM")[0] if person_data.get("parentM") else None
        )

        parents = person.get_parents()

        result_text.delete(1.0, END)
        result_text.insert(END, f"Parents of {name}:\n")
        for parent in parents:
            result_text.insert(END, f"- {parent}\n" if parent else "- Unknown\n")
    else:
        result_text.delete(1.0, END)
        result_text.insert(END, "Person not found in data.\n")

def show_grandchildren():
    name = selected_name.get()
    if name == "Select a name":
        result_text.delete(1.0, END)
        result_text.insert(END, "Please select a name from the list.\n")
        return

    if name in people_data:
        person_data = people_data[name]
        person = Person(
            name=person_data["name"],
            birth_date=person_data.get("birth_date"),
            death_date=person_data.get("death_date"),
            parentF=person_data.get("parentF")[0] if person_data.get("parentF") else None,
            parentM=person_data.get("parentM")[0] if person_data.get("parentM") else None
        )

        grandchildren = person.get_grandchildren()

        result_text.delete(1.0, END)
        result_text.insert(END, f"Grandchildren of {name}:\n")
        if grandchildren:
            for grandchild in grandchildren:
                result_text.insert(END, f"- {grandchild}\n")
        else:
            result_text.insert(END, "No grandchildren found.\n")
    else:
        result_text.delete(1.0, END)
        result_text.insert(END, "Person not found in data.\n")

def show_immediate_family():
    name = selected_name.get()
    if name == "Select a name":
        result_text.delete(1.0, END)
        result_text.insert(END, "Please select a name from the list.\n")
        return
def show_extended_family():
    name = selected_name.get()
    if name == "Select a name":
        result_text.delete(1.0, END)
        result_text.insert(END, "Please select a name from the list.\n")
        return

def search_immediate_family():

    name = selected_name.get()

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

    name = selected_name.get()

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

def show_siblings():
    name = selected_name.get()
    if name == "Select a name":
        result_text.delete(1.0, END)
        result_text.insert(END, "Please select a name from the list.\n")
        return

    if name in people_data:
        person_data = people_data[name]
        person = Person(
            name=person_data["name"],
            birth_date=person_data.get("birth_date"),
            death_date=person_data.get("death_date"),
            parentF=person_data.get("parentF")[0] if person_data.get("parentF") else None,
            parentM=person_data.get("parentM")[0] if person_data.get("parentM") else None
        )

        siblings = person.get_siblings()

        result_text.delete(1.0, END)
        result_text.insert(END, f"Siblings of {name}:\n")
        if siblings:
            for sibling in siblings:
                result_text.insert(END, f"- {sibling}\n")
        else:
            result_text.insert(END, "No siblings found.\n")
    else:
        result_text.delete(1.0, END)
        result_text.insert(END, "Person not found in data.\n")

def show_cousins():
    name = selected_name.get()
    if name == "Select a name":
        result_text.delete(1.0, END)
        result_text.insert(END, "Please select a name from the list.\n")
        return

    if name in people_data:
        person_data = people_data[name]
        person = Person(
            name=person_data["name"],
            birth_date=person_data.get("birth_date"),
            death_date=person_data.get("death_date"),
            parentF=person_data.get("parentF")[0] if person_data.get("parentF") else None,
            parentM=person_data.get("parentM")[0] if person_data.get("parentM") else None
        )

        cousins = person.get_cousins()

        result_text.delete(1.0, END)
        result_text.insert(END, f"Cousins of {name}:\n")
        if cousins:
            for cousin in cousins:
                result_text.insert(END, f"- {cousin}\n")
        else:
            result_text.insert(END, "No cousins found.\n")
    else:
        result_text.delete(1.0, END)
        result_text.insert(END, "Person not found in data.\n")

#TASK F2b
#Task F2b i
# Show the list of family birthday
def search_branch_birthdays():
   name = selected_name.get()
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
       birthdays = person.get_branch_birthdays()
       result_text.delete(1.0, END)
       if birthdays:
           result_text.insert(END, f"Family branch birthdays for {name}:\n" + "\n".join(birthdays))
       else:
           result_text.insert(END, f"No birthdays found for the branch of {name}.")
   else:
       result_text.delete(1.0, END)
       result_text.insert(END, "Person not found in the database.\n")


# Adding new method for birthday calendar

def create_birthday_calendar():
   calendar = defaultdict(list)
   for person, details in people_data.items():
       if "birth_date" in details:
           birth_date = details["birth_date"]
           # Get month and day
           month_day = "-".join(birth_date.split("-")[1:])
           calendar[month_day].append(details["name"])

   # Turn to an organized calendar
   sorted_calendar = dict(sorted(calendar.items(), key=lambda x: (int(x[0].split("-")[0]), int(x[0].split("-")[1]))))
   return sorted_calendar

#Task F2b ii
def show_birthday_calendar():
   calendar = create_birthday_calendar()  # Создаём упорядоченный календарь
   result_text.delete(1.0, END)  # Очистка текстового поля
   result_text.insert(END, "Birthday Calendar:\n")
   for date, people in calendar.items():
       people_list = ", ".join(people)
       result_text.insert(END, f"{date}: {people_list}\n")

#Task F3b i
def count_children():
    children_count = defaultdict(int)
    for child, details in people_data.items():
        # Checking the child's parents and replacing None with an empty list
        fathers = details.get("parentF") or []
        mothers = details.get("parentM") or []

        # Iterating through the lists of parents
        for father in fathers:
            children_count[father] += 1
        for mother in mothers:
            children_count[mother] += 1

    return dict(children_count)


def display_children_count():

    children_count = count_children()  # Получаем словарь с подсчётом детей
    result_text.delete(1.0, END)  # Очистка текстового поля
    result_text.insert(END, "Children Count:\n")

    for person, count in children_count.items():

        result_text.insert(END, f"{person}: {count} children\n")

def calculate_average_children():

    children_count = count_children()
    total_people = len(people_data)  # Всего людей в дереве
    total_children = sum(children_count.values())  # Сумма всех детей

    # Divide by 0 protection

    if total_people == 0:

        return 0

    return total_children // total_people
def display_average_children():

    average_children = calculate_average_children()
    result_text.delete(1.0, END)  #Clearing a text field
    result_text.insert(END, f"Average number of children per person: {average_children:.2f}\n")

# Task F3b ii
def show_average_age_at_death():
       average_age = Person.calculate_average_age_at_death()
       result_text.delete(1.0, END)
       result_text.insert(END, f"Average age at death: {average_age:.2f}\n")

#Set up of Tkinder window

root = Tk()
root.title("Family Tree Explorer")
root.geometry("600x700")
sorted_names = sorted(people_data.keys(), key=lambda name: name.split()[-1])
#Variable to store the selected name
selected_name = StringVar()
selected_name.set("Select a name")  # Initial value
#Label and drop-down list for selecting a name
Label(root, text="Family Tree Explorer").pack(pady=5)
name_menu = OptionMenu(root, selected_name, *sorted_names)
name_menu.pack(pady=5)

# Adding buttons with individual calls .pack()
Button(root, text="Show Parents", command=show_parents, width=20).pack(pady=5)
Button(root, text="Show Grandchildren", command=show_grandchildren, width=20).pack(pady=5)
Button(root, text="Show Immediate Family", command=search_immediate_family, width=20).pack(pady=5)
Button(root, text="Show Extended Family", command=search_extended_family, width=20).pack(pady=5)
Button(root, text="Show Siblings", command=show_siblings, width=20).pack(pady=5)
Button(root, text="Show Cousins", command=show_cousins, width=20).pack(pady=5)
Button(root, text="Show Branch Birthdays", command=search_branch_birthdays, width=20).pack(pady=5)
Button(root, text="Show Birthday Calendar", command=show_birthday_calendar, width=20).pack(pady=5)
Button(root, text="Show Age at Death", command=show_average_age_at_death, width=20).pack(pady=5)
Button(root, text="Show Children Count", command=display_children_count, width=20).pack(pady=5)
Button(root, text="Show Average Children", command=display_average_children, width=20).pack(pady=5)
# Create a text field to display the results
result_text = Text(root, height=10, width=50)
result_text.pack(pady=5)
# Launch the main window Tkinter
root.mainloop()