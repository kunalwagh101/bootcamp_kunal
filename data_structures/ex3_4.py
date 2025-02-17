"""NO 8 .Aggregate data from different structures.
No.9 Calculate the total number of unique stations served by both buses and trains."""

from ex3_3 import schedules
from ex3_2 import handle_unique



def no_unique() :

    bus_stations = [ station[1] for stations in schedules().values() for station in stations ]
    unique = handle_unique()
    all_unique_stations = set(bus_stations).union(unique)
    
    return list(all_unique_stations)

if __name__ == "__main__" :
    print(no_unique())
