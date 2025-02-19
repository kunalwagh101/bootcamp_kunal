""""NO.17 Utilize Counter from the collections module to analyze data.
No.18 Use a Counter to find the most frequented stations in the network."""



from collections import Counter
from ex3_4 import no_unique


def find_counter() :
    station_visits = no_unique()

    station_counter = Counter(station_visits)
    most_common_station = station_counter.most_common(1)
    return most_common_station



if __name__ == "__main__" :
    print(find_counter())