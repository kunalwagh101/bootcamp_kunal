"""No.19 Apply custom sorting to collection data.
No.20 Sort the bus routes based on the number of stops, using a custom sorting function."""

from ex3_3 import schedules 


def bus_sort() :
    bus_schedules = schedules()

    sorted_routes = sorted(bus_schedules.items(), key=lambda item: len(item[1]))

    print("Bus routes sorted by number of stops:")
    for route, schedule in sorted_routes:
        print(f"  {route}: {len(schedule)} stops")

    return bus_sort


if __name__ == "__main__" :
    print(bus_sort())