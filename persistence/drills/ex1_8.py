import pickle

class Military:
    def __init__(self, name, rank, unit, security_clearance, mission):
        self.name = name
        self.rank = rank
        self.unit = unit
        self.security_clearance = security_clearance 
        self.mission = mission  

    def __getstate__(self):

        state = self.__dict__.copy()
        for sensitive_attr in ["security_clearance", "mission"]:
            state.pop(sensitive_attr, None)  #
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.security_clearance = "Classified"
        self.mission = "Classified"

    def serialize(self):
        return pickle.dumps(self)

    @classmethod
    def deserialize(cls, data) :
        return pickle.loads(data)


if __name__ == "__main__":
    soldier = Military("tiger", "Captain", "sp9", "higer", "snow leapord")
    serialized_data = soldier.serialize()
    restored_soldier = Military.deserialize(serialized_data)
    
    print(vars(restored_soldier))
