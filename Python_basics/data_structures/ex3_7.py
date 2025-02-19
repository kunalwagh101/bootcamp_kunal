""" no 15 : Handle complex nesting in data structures.
no 16 Create a nested data structure that maps a transport line to its schedule, and each schedule to a list of passengers (by name)."""

def nested_fun() : 
    transport_passengers = {
        "Route A": {
            "08:00": ["Alice", "Bob"],
            "08:15": ["Charlie"],
        },
        "Red Line": {
            "09:00": ["Dave", "Eve"],
            "09:15": ["Frank", "Grace"],
        },
    }

    print("Transport line passenger data:")
    for line, schedule in transport_passengers.items():
        print(f"  {line}:")
        for time, passengers in schedule.items():
            print(f"    {time}: {passengers}")



if __name__ == "__main__" :
    print(nested_fun())