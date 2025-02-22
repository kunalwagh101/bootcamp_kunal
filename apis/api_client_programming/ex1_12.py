"""
Query Pokémon Data

Objective: Access data on Pokémon via the PokéAPI.
Task: Create a Python script that fetches data about a specific Pokémon from https://pokeapi.co/api/v2/pokemon/{name} and prints its types.
Expected Output: The types of the specified Pokémon
"""

import requests

def get_url(name):
    url  =  f"https://pokeapi.co/api/v2/pokemon/{name}"
    responce  =  requests.get(url)
    return  responce.json() if responce.status_code == 200 else []

def main():
    name = input("Name the pokemon =")  or "Pikachu"
    data  =  get_url(name)
    char_name  =  data["name"]
    type_char  =  data["types"][0]["type"]["name"]
    print(char_name, type_char)
   

    
if __name__ =="__main__" :
    main()