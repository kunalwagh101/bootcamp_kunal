"""
Get User Details from GitHub

Objective: Retrieve user details from GitHub using their REST API.
Task: Create a command line program that takes a GitHub username as an argument and fetches 
details about the user (https://api.github.com/users/{username}).
Expected Output: The specified user's details, such as name and public repos count.

"""

import typer
import requests
def user_details(username:str) -> str :
    url = "https://api.github.com/users/"+username
    response =  requests.get(url)

    info  = response.json()
    public_repos =  info["public_repos"]
    login =  info["login"]
    name =  info["name"] or "not available"
    
    print( f" login= {login} , name = {name}, public_repos = {public_repos}"  )




app =  typer.Typer()

@app.command()
def main(name:str = "e9kwagh"):
    return user_details(name)


if __name__ == "__main__" :
    app()