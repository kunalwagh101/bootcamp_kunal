"""
No.11 Fetch and Display Hacker News Posts

Objective: Retrieve top posts from Hacker News.
Task: Use the requests library to fetch the top posts from Hacker News (https://hacker-news.firebaseio.com/v0/topstories.json) and print their titles and URLs.
Expected Output: Titles and URLs of the top posts on Hacker News.
"""

import requests 

def get_url():
    response  =  requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    return response.json() if response.status_code == 200 else []



def get_post(pid):
    url = f"https://hacker-news.firebaseio.com/v0/item/{pid}.json"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else {}


def show(posts):
    for p in posts:
        title = p.get("title")
        url = p.get("url", )
        print(f"Title = {title}")
        print(f"URL = {url}\n")


def main():
    ids = get_url()
    top_ids = ids[:10]
    ps = [get_post(i) for i in top_ids]
    show(ps)



if __name__ =="__main__" :
    main()