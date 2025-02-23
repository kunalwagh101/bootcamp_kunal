"""
No.1 Basic Serialization with Pickle: Serialize a simple Person object to a file using Pickle.
Create a Person class with attributes name, educational institutions (a list) and 
colleagues and use pickle to serialize an instance of this class.
"""
from pathlib import Path
import pickle
import csv
class Person:
    def __init__(self, name, educational_institutions, colleagues):
        self.name = name
        self.educational_institutions = educational_institutions
        self.colleagues = colleagues

    def __repr__(self):
        return f"Person(name={self.name}, educational_institutions={self.educational_institutions}, colleagues={self.colleagues})"

    def serialization(self,obj):
        with open("ex_1.pkl","wb") as f:
            pickle.dump(obj,f)
            return f"serialization done !"

    def serialise(self,filename = "ex_1_new.pkl"):
        with open(filename ,"wb") as f:
            pickle.dump(self,f)
            return f"serialization done !"
        
    def obj_to_csv(self,filename ="ex_1.csv") :
        with open(filename ,"w" ) as f :
            csv_file = csv.writer(f)
            csv_file.writerow(["name" , "educational_institutions","colleagues" ])
            csv_file.writerow([self.name , ",".join(self.educational_institutions), ",".join(self.colleagues)])
            return "converted to csv "
  
    """
    No.2 Deserialization with Pickle: Deserialize the Person object back into Python.
    Read the serialized file and recreate the Person object using pickle.
    """

    def deserialise(self):
        all_pkl = Path.cwd().glob("ex_1*.pkl")
        for pkl in all_pkl :
            with open(pkl,"rb") as f:
              yield pickle.load(f)

    def all_print(self):
        info_obj = []
        for i in self.deserialise():
            print(i)
            info_obj.append(i)
        
if __name__ == "__main__":

    person = Person(name="Kunal Wagh",educational_institutions=["MET", "NIT"], colleagues=["a1", "a2"])
    person.serialization(person)
    person.serialise()
    person.obj_to_csv()
    person.all_print()




# with open("person.pkl", "wb") as file:
#     pickle.dump(person, file)

# print("Serialization complete. Object saved to 'person.pkl'.")


# with open("person.pkl", "rb") as file:
#     loaded_person = pickle.load(file)

# print("Deserialization complete. Loaded object:", loaded_person)
