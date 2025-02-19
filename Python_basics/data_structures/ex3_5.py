
"""
No 10 .Implement named tuples for more structured data.
No.11 Define a named tuple Schedule with fields for time and station.
No.12 Refactor the earlier schedules to use Schedule named tuples.
"""

from collections import namedtuple
from ex3_3 import schedules

def refractor() :

    Schedule = namedtuple("Schedule", ["time", "station"])

    bus_schedules = {
        "Route A": [Schedule("08:00", "Stop 1"),
                    Schedule("08:15", "Stop 2"),
                    Schedule("08:30", "Stop 3")],
        "Route B": [Schedule("09:00", "Stop 4"),
                    Schedule("09:15", "Stop 5")],
    }

    print("Bus Schedules using named tuples:")
    for route, schedules in bus_schedules.items():
        print(f"  {route}:")
        for entry in schedules:
            print(f"    At {entry.time} -> {entry.station}")




if __name__ == "__main__" :
    print(refractor())
