"""
No.11 Serialization of Custom Collections: Serialize a custom collection class, like MyCollection, containing various objects.
Implement serialization and deserialization methods for the MyCollection class.
"""




import pickle

class MyCollection:
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def add(self, item):
        self.items.append(item)

    def __iter__(self):
        return iter(self.items)

    def __repr__(self):
        return f"MyCollection({self.items!r})"

    def serialize(self):
        return pickle.dumps(self)

    @classmethod
    def deserialize(cls, serialized_data):
        return pickle.loads(serialized_data)



if __name__ == '__main__':
    collection = MyCollection()
    collection.add({'key': 'value'})
    collection.add([1, 2, 3])
    collection.add("example")

    serialized = collection.serialize()

   
    new_collection = MyCollection.deserialize(serialized)

    print("Original Collection:", collection)
    print("Deserialized Collection:", new_collection)
