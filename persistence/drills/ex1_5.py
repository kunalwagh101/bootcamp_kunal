"""
No.5 YAML Serialization: Serialize a Car object to a YAML format.
Use a library like PyYAML to serialize a Car instance into YAML.
"""


import yaml

class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def to_yaml(self):
        return yaml.dump(self.__dict__, default_flow_style=False)

    @classmethod
    def from_yaml(cls, yaml_str):
        data = yaml.safe_load(yaml_str)
        return cls(**data)

if __name__ == "__main__" :
    car = Car("Tesla", "Model S", 2023)

    yaml_data = car.to_yaml()
    print("Serialized YAML:\n", yaml_data)


    car_obj = Car.from_yaml(yaml_data)
    print("\nDeserialized Object:", car_obj.__dict__)
