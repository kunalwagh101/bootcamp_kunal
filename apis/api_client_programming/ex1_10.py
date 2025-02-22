""""
No.10 GraphQL Query for AniList Anime Data

Objective: Fetch and display anime information using AniList's GraphQL API.
Task: Use gql to query AniList for information on an anime by its title.
GraphQL Endpoint: https://graphql.anilist.co
Expected Output: The title, description, and airing status of the anime.
"""

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def get_anime(qry):
    tr = RequestsHTTPTransport(url="https://graphql.anilist.co", verify=True, retries=3)
    client = Client(transport=tr, fetch_schema_from_transport=True)
    query_str = gql("""
    query ($q: String) {
      Media(search: $q, type: ANIME) {
        title { romaji }
        description
        status
      }
    }
    """)
    res = client.execute(query_str, variable_values={"q": qry})
    return res.get("Media", {})

def show(anime):
    title = anime.get("title", {}).get("romaji", "N/A")
    disc = anime.get("description", "N/A")
    status = anime.get("status", "N/A")
    print(f"Title: {title}")
    print(f"Description: {disc}")
    print(f"Status: {status}")

def main():
    qry = input("Anime Title (default: Naruto): ") or "Naruto"
    anime = get_anime(qry)
    show(anime)

if __name__ == "__main__":
    main()
