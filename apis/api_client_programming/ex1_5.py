"""
Post a message using Blueskey app API

Objective: Use the Bluesky API to post a short 'tweet'.
Task: Write a script that posts a message to your Bluesky account.
API Endpoint: Refer to Bluesky's API documentation for posting tweets.
Expected Output: A tweet is posted to your account.

"""
import requests
import typer
from datetime import datetime, timezone
import json

def cli(identifier:str , password:str):
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    BLUESKY_HANDLE =  identifier
    BLUESKY_APP_PASSWORD = password

    resp = requests.post(
    "https://bsky.social/xrpc/com.atproto.server.createSession",
    json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
            )
    
    resp.raise_for_status()
    session =  resp.json()
    print(session["accessJwt"])


    post = {
    "$type": "app.bsky.feed.post",
    "text": "Hello World!",
    "createdAt": now,
        }

    send_tweet = requests.post(   
    "https://bsky.social/xrpc/com.atproto.repo.createRecord",
    headers={"Authorization": "Bearer " + session["accessJwt"]},
    json={
        "repo": session["did"],
        "collection": "app.bsky.feed.post",
        "record": post,
    },
)

    send_tweet.raise_for_status()

    print(json.dumps(resp.json(), indent=2))  
    




