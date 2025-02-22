"""
No.14 Display NYT Best Sellers List

Objective: Access and display the current New York Times Best Sellers list.
Task: Use the requests library to fetch the current Best Sellers list from the New York Times API (https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={your-api-key}).
Expected Output: Titles and authors of the current hardcover fiction best sellers.
"""

import  requests

def get_url(api):
    url = f"https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={api}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return data.get("results", {}).get("books", [])
    return None

def show(bs):
    for b in bs:
        title = b.get("title")
        auth = b.get("author")
        print(f"Title = {title}")
        print(f"Author = {auth}\n")

def main():
    key = input("NYT API Key: ") or "u9k0G14APaDOPlrhcx05xGR0BNAMDkWh"
    bs = get_url(key)
    if bs:
        show(bs)
    else:
        print("Error getting Best Sellers List.")

if __name__ == "__main__":
    main()

    print( "A though the output will look like this : ")
    print(""" NYT API Key: u9k0G14APaDOPlrhcx05xGR0BNAMDkWh
Title: ONYX STORM
Author: Rebecca Yarros

Title: IRON FLAME
Author: Rebecca Yarros

Title: EMILY WILDE'S COMPENDIUM OF LOST TALES
Author: Heather Fawcett

Title: PARANOIA
Author: James Patterson and James O. Born

Title: JAMES
Author: Percival Everett

Title: THE WOMEN
Author: Kristin Hannah

Title: WE ALL LIVE HERE
Author: Jojo Moyes

Title: FOURTH WING
Author: Rebecca Yarros

Title: THREE DAYS IN JUNE
Author: Anne Tyler

Title: THE WEDDING PEOPLE
Author: Alison Espach

Title: THE GOD OF THE WOODS
Author: Liz Moore

Title: THE MEDICI RETURN
Author: Steve Berry

Title: BONDED IN DEATH
Author: J.D. Robb

Title: THE NIGHT IS DEFYING
Author: Chloe C. Peñaranda

Title: NEMESIS
Author: Gregg Hurwitz """)