"""
No.13 Fetch User Contributions on GitHub

Objective: Use the GitHub REST API to fetch a user's contributions.
Task: Write a command line program that takes a GitHub username and fetches the number of contributions in the last year.
API Endpoint: Use GitHub's API to construct a query for contributions. Note: This may require parsing HTML or leveraging unofficial APIs.
Expected Output: The number of contributions made by the user in the last year.



"""


import requests

def get_url(usr):
    url = f"https://github-contributions-api.deno.dev/{usr}"
    response = requests.get(url)
    return response if response.status_code == 200 else None

def main():
    # usr = input("GitHub Username : ") or "e9kwagh"
    user = "e9kwagh"
    total = get_url(user)
    print("total number of contribution lat year  = ", total.text[0])

if __name__ == "__main__":
    main()