"""
No.3 List Public Events on GitHub

Objective: Access and display GitHub's public events.
Task: Use requests to fetch and print the recent public events 
from GitHub (https://api.github.com/events).
Expected Output: A summary of recent public events on GitHub.
"""

import requests
def main() :
    response = requests.get("https://api.github.com/events")
    events = response.json()
    print("events =" ,events[0])
    # text = response.text
    # with open("output.txt","w",encoding="utf-8") as f:
    #     for line in text:
    #         f.write(line)



if __name__ == "__main__":
    main()