"""No .21 Combine different data structures to model a comprehensive transportation system.
Create a class TransportNetwork that integrates all the previous data structures and provides methods to add routes, update schedules, and add passenger"""

from collections import defaultdict, namedtuple, Counter


Schedule = namedtuple("Schedule", ["time", "station"])

class TransportNetwork:
    def __init__(self):       
        self.bus_routes = {}      
        self.train_lines = {}     
        self.passengers_count = defaultdict(int)      
        self.transport_passengers = defaultdict(lambda: defaultdict(list))
    
    def add_bus_route(self, route_name, schedule_list):
        """
        Add a bus route with its schedule.
        schedule_list: list of tuples (time, station) or Schedule named tuples.
        """
        converted_schedule = []
        for entry in schedule_list:
            
            if isinstance(entry, tuple):
                converted_schedule.append(Schedule(*entry))
            else:
                converted_schedule.append(entry)
        self.bus_routes[route_name] = converted_schedule
    
    def add_train_line(self, line_name, stations):
        self.train_lines[line_name] = stations
    
    def update_schedule(self, transport_line, time, station, passengers=None):
        """
        Update schedule for a given transport line.
        Adds a new schedule entry and optionally records passengers boarding at that time.
        """
        if passengers is None:
            passengers = []
        self.transport_passengers[transport_line][time].extend(passengers)
    
    def add_passenger(self, station, passenger_name):
        """
        Increment the passenger count for a given station.
        """
        self.passengers_count[station] += 1
    
    def get_unique_stations(self):
        """
        Return a set of all unique stations served by both bus routes and train lines.
        """
        unique_stations = set()
       
        for schedule in self.bus_routes.values():
            for entry in schedule:
                unique_stations.add(entry.station)
       
        for stations in self.train_lines.values():
            unique_stations.update(stations)
        return unique_stations
    
    def most_frequent_station(self):
        """
        Use Counter to determine the station with the highest passenger count.
        """
        station_visits = Counter(self.passengers_count)
        return station_visits.most_common(1)[0] if station_visits else None


if __name__ == "__main__":
    network = TransportNetwork()
    
    
    network.add_bus_route("Route A", [("08:00", "Stop 1"),
                                        ("08:15", "Stop 2"),
                                        ("08:30", "Stop 3")])
    network.add_bus_route("Route B", [("09:00", "Stop 4"),
                                        ("09:15", "Stop 5")])
    
    network.add_train_line("Red Line", ["Station 1", "Station 2", "Station 3"])
    network.add_train_line("Blue Line", ["Station 4", "Station 5", "Station 6"])
    

    network.update_schedule("Route A", "08:00", "Stop 1", ["Alice", "Bob"])
    network.update_schedule("Red Line", "09:00", "Station 1", ["Charlie", "Dave"])

    network.add_passenger("Stop 1", "Eve")
    network.add_passenger("Station 1", "Frank")
    

    unique_stations = network.get_unique_stations()
    print("Unique stations in the network:", unique_stations)
    

    most_freq = network.most_frequent_station()
    print("Most frequented station:", most_freq)
