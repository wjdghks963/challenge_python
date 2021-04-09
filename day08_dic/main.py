from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")


def get_index(post):
    url = post.find("a", {"class", "SQnoC3ObvgnGjWt90zD9Z"})
    if url:
        article = post.find("h3").text
        votes = post.find("div", {"class", "_1rZYMD_4xY3gRcSS3p8ODO"}).text
        url = url.attrs["href"]
        return {
            "article": article,
            "votes": votes,
            "url": f"https://www.reddit.com/{url}",
        }


def get_subreddit(submited_subreddit):
    subreddit = dict(language="", posts=[])
    subreddit["language"] = submited_subreddit

    url = f"https://www.reddit.com/r/{submited_subreddit}/top/?t=month"
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")

    posts_container = soup.find("div", {"class", "rpBJOHq2PR60pnwJlUyP0"})
    posts_list = posts_container.find_all("div", {"class": None}, recursive=False)

    for post in posts_list:
        extracted_post = get_index(post)
        if extracted_post:
            subreddit["posts"].append(extracted_post)
    return subreddit


def get_subreddits(submited_subreddits_dict):
    subreddits = []
    for submited_subreddit in submited_subreddits_dict:
        subreddit = get_subreddit(submited_subreddit)
        print(subreddit)
        subreddits.append(subreddit)
    return subreddits


@app.route('/')
def index():
    return render_template("home.html", subreddits=subreddits)


@app.route('/read')
def reddit():

    submited_subreddits_dict = request.args.to_dict()
    subreddits = get_subreddits(submited_subreddits_dict)
    return render_template("read.html", subreddits=subreddits)

app.run(host="0.0.0.0")