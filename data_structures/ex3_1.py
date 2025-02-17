"""No 1.Familiarize yourself with basic data structures
 by creating lists and dictionaries for bus routes and train lines.
 NO.2 Create a list of bus routes.
 NO.3 Create a dictionary mapping train lines to their respective stations.
 """


def routes_lines():

    bus_routes = ["Route A", "Route B", "Route C"]

    train_lines = {
    "Mumbai Line": ["Station 1", "Station 2", "Station 3" ,"Station 6"],
    "Pune Line": ["Station 4", "Station 5", "Station 6"],
    }

    return  bus_routes,train_lines

if __name__ == "__main__" :
    
    print("Bus Routes:", routes_lines()[0])
    print("Train Lines:", routes_lines()[1])
