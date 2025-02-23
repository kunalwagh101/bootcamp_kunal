"""
No.6 YAML Deserialization: Deserialize the YAML back into a Car object.
Read the YAML string and convert it back into a Car instance.

"""

import yaml
from ex1_5 import Car

class  Convert(Car):
    def __init__ (self, brand, model, year ) :
        super().__init__( brand, model, year)
        self.obj = Car( self.brand, self.model, self.year)

    def to_yml(self):
        return self.obj.to_yaml()

    @classmethod 
    def to_obj(cls,data):
        obj_data =  yaml.safe_load(data)   
        return  cls(**obj_data) 
    
if __name__ == "__main__" :
    con =  Convert("BWM" , "M5" ,"2022")
    yml_str = con.to_yml()
    print("convertd to yml  : ", yml_str)
    obj_str =  Convert.to_obj(yml_str)
    print("onverted back to object:" , obj_str)

