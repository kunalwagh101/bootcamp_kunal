"""
No.1 Fetch Public GitHub Repositories

Objective: Use the GitHub REST API to fetch public repositories.
Task: Write a Python script that uses the requests library to get a few of public repositories from the GitHub API (https://api.github.com/repositories) and prints the names.
Expected Output: A list of public repository names printed to the console.
"""

import requests
def main():
    response =  requests.get("https://api.github.com/repositories")
    respos =  response.json()
    for repo in respos[:10]:
        print(repo["name"])
        

if __name__ == "__main__" :
    main()