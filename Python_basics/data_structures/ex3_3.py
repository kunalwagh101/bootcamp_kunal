
""" NO.6 Understand nested data structures by organizing schedules.
NO.7 Create a dictionary where each key is a route, and the value is a list of tuples
 representing scheduled stops (time, station)."""




def schedules() :

    schedule = {
    "Route A": [("08:00", "Stop 1"), ("08:15", "Stop 2"), ("08:30", "Stop 3")],
    "Route B": [("09:00", "Stop 4"), ("09:15", "Stop 5")]}

    return schedule

if __name__ == "__main__" :
    print(schedules())


