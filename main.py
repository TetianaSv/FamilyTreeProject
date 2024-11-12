from tkinter import Tk, Label, Entry, Button, Text, END
from data import people_data

class Person:

    def __init__(self, name, birth_date=None, death_date=None, parentF=None, parentM=None):

        self.name = name

        self.birth_date = birth_date

        self.death_date = death_date

        self.parentF = parentF

        self.parentM = parentM

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

# Function for searching of relatives

def search_family_info():

    name = entry.get()

    if name in people_data:

        data = people_data[name]

        person = Person(

            name=data["name"],
            birth_date=data["birth_date"],
            death_date=data["death_date"],
            parentF=data["parentF"][0] if data["parentF"] else None,
            parentM=data["parentM"][0] if data["parentM"] else None
        )

        parents = person.get_parents()
        grandparents = person.get_grandparents()
        result_text.delete(1.0, END)
        result_text.insert(END, f"Parents of {name}: {parents}\n")
        result_text.insert(END, f"Grandparents of {name}: {grandparents}\n")

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
button = Button(root, text="Search", command=search_family_info)
button.pack(pady=5)
result_text = Text(root, height=10, width=50)
result_text.pack(pady=5)
root.mainloop()