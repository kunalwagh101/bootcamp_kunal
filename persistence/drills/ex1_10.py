import json

class UserV1:
   
    def __init__(self, username, age):
        self.version = 1
        self.username = username
        self.age = age

    def serialize(self):
        return json.dumps(self.__dict__)

class UserV2:

    def __init__(self, username, age, role="user"):
        self.version = 2
        self.username = username
        self.age = age
        self.role = role  


    @classmethod
    def deserialize(cls, json_str):
        data = json.loads(json_str)
        if data.get("version") == 1:
            print("Detected old version, applying migration...")
            return cls(data["username"], data["age"])
        
        return cls(data["username"], data["age"], data.get("role", "user"))
    

    def serialize(self):
        """Convert object to JSON"""
        return json.dumps(self.__dict__)

if __name__ == "__main__" :
    old_user = UserV1("kunal_dev", 24)
    old_serialized = old_user.serialize()


    new_user = UserV2.deserialize(old_serialized)

    print(f"Username: {new_user.username}, Age: {new_user.age}, Role: {new_user.role}")
