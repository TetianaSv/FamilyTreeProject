import unittest
from main import Person  # Importing the Person class from the main file

class TestPerson(unittest.TestCase):
   def setUp(self):
       # Creating test objects based on people_data
       self.otto = Person(
           name="Otto Emmersohn",
           birth_date="1974-04-15",
           death_date=None,
           parentF="Hans Emmersohn",
           parentM="Greta Becker",
           spouse=["Cornelia Emmersohn"]
       )
       self.cornelia = Person(
           name="Cornelia Emmersohn",
           birth_date="1972-10-23",
           death_date="2015-02-07",
           parentF="Thomas Smith",
           parentM="Priya Smith",
           spouse=["Otto Emmersohn"]
       )
       self.joy = Person(
           name="Joy Emmersohn",
           birth_date="1995-03-03",
           death_date=None,
           parentF="Cornelia Emmersohn",
           parentM="Otto Emmersohn",
           spouse=None
       )
       self.arnold = Person(
           name="Arnold Emmersohn",
           birth_date="1995-03-03",
           death_date=None,
           parentF="Cornelia Emmersohn",
           parentM="Otto Emmersohn",
           spouse=None
       )
   def test_get_siblings(self):
       # Checking the get_siblings method for the Joy object
       siblings = self.joy.get_siblings()
       self.assertIn("Arnold Emmersohn", siblings)  # Joy and Arnold are siblings
       self.assertNotIn("Cornelia Emmersohn", siblings)  # Parents aren't included in siblings
       self.assertEqual(len(siblings), 1)  # Joy only has one brother
   def test_get_parents(self):
       # Checking the get_parents method for the Joy object
       parents = self.joy.get_parents()
       self.assertIn("Cornelia Emmersohn", parents)
       self.assertIn("Otto Emmersohn", parents)
       self.assertEqual(len(parents), 2)  # Joy has 2 parents
   def test_get_cousins(self):
       # Checking the get_cousins method for the Joy object
       cousins = self.otto.get_cousins()
       self.assertIn("Erik Emmersohn", cousins)  # Erik - cousin via Thomas Smith
       self.assertNotIn("Arnold Emmersohn", cousins)  # Siblings are not included
       self.assertGreaterEqual(len(cousins), 1)  # Joy has at least one cousin
if __name__ == "__main__":
   unittest.main()