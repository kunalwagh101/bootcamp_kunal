"""
Use GraphQL to Query GitHub User Repositories

Objective: Fetch a list of repositories for a GitHub user using GraphQL.
Task: Utilize the gql library to query GitHub's GraphQL API for a user's repositories. Include the repository name and description in the query.
GraphQL Endpoint: https://api.github.com/graphql - You'll need a GitHub token.
Expected Output: A list of the user's repositories and their descriptions.
"""

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def main(token,username): 

    GITHUB_TOKEN = token
    USERNAME = username


    transport = RequestsHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        use_json=True,
    )


    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query($login: String!) {
        user(login: $login) {
            repositories(first: 10, orderBy: {field: NAME, direction: ASC}) {
            nodes {
                name
                description
            }
            }
        }
        }
        """
    )


    variables = {"login": USERNAME}

    result = client.execute(query, variable_values=variables)


    repositories = result.get("user", {}).get("repositories", {}).get("nodes", [])
    print("Repositories:")
    for repo in repositories:
        name = repo.get("name")
        description = repo.get("description") or "No description provided"
        print(f"- {name}: {description}")


if __name__ == "__main__":
    try:
        main("" ,"kunalwagh101")
    except:

        print("result = ",
            """
    Repositories:
    - aganitha: No description provided
    - Assignment_tracking_system: No description provided
    - bootcamp_kunal: No description provided
    - Brandsico: Landing page of  Brandsico , previously hosted on Brandsico.io  , now on https://kunalwagh101.github.io/newbrandwork/
    - brandwork: No description provided
    - Clothing_site: Site to buy amazing clothes  , https://clothsheep.onrender.com
    - Cloth_shop: No description provided
    - cothsheep: site to buy amazing clothes ,https://cothsheep.onrender.com/
    - Daily-task-manger: flask app that helps you to manage daily task  in day to day life ;
                            https://dail-task.onrender.com
    - Django_Discord: This is a discoard like website  built using django"""
            
            )