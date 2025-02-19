"""No.13 Explore default dictionaries for handling missing keys gracefully.
NO.14 Create a default dictionary for tracking the number of passengers per station."""
from collections import defaultdict
from ex3_4 import no_unique

passengers_count = defaultdict(int)


def random_passengers() :
    stations = no_unique()


    for station in stations:
        passengers_count[station] += 1

    print("Passenger counts per station:")
    for station, count in passengers_count.items():
        print(f"  {station}: {count}")
    return passengers_count


if __name__ == "__main__" :
    print(random_passengers())