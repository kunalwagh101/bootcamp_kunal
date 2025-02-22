"""
No.9 Access Rick and Morty Characters

Objective: Fetch character information from "The Rick and Morty API".
Task: Write a script to get and display information about characters from "The Rick and Morty API" (https://rickandmortyapi.com/api/character).
Expected Output: Information about the characters, such as names and species
"""

import requests

def get_chars():
    url = "https://rickandmortyapi.com/api/character"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json().get("results", [])
    return []

def show_chars(chars):
    for c in chars:
        print(f"Name: {c['name']}, Species: {c['species']}")

def main():
    chars = get_chars()
    show_chars(chars)

if __name__ == "__main__":
    main()
