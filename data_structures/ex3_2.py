"""NO 4. Use sets to handle unique elements in the transportation system.

No5. Create a set of all unique stations in the system."""


from ex3_1 import routes_lines


def handle_unique():
      unique_items = {  station for stations in routes_lines()[1].values() for station in stations}
      return unique_items


if __name__ == "__main__" :
    print(handle_unique())