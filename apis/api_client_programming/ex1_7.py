import requests

def fetch_latest_launch():
    url = "https://spacex-production.up.railway.app/graphql/"
    query = """
    {
      launches(limit: 1, sort: "launch_date_utc", order: "desc") {
        mission_name
        launch_date_utc
        rocket {
          rocket_name
        }
        launch_site {
          site_name_long
        }
        links {
          video_link
        }
      }
    }
    """
    response = requests.post(url, json={'query': query})
    
    if response.status_code == 200:
        data = response.json()
        launch = data.get("data", {}).get("launches", [])[0]
        if launch:
            print("Mission Name:", launch["mission_name"])
            print("Launch Date (UTC):", launch["launch_date_utc"])
            print("Rocket Name:", launch["rocket"]["rocket_name"])
            print("Launch Site:", launch["launch_site"]["site_name_long"])
            print("Video Link:", launch["links"]["video_link"] or "N/A")
        else:
            print("No launch data available.")
    else:
        print("Failed to fetch data. Status Code:", response.status_code)

if __name__ == "__main__":
    fetch_latest_launch()
