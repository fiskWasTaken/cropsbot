import requests
import json
import urllib

base = 'https://e621.net'


def get_latest(tags="", limit=1):
    """
    Get the latest image(s) with these filters
    """
    return json.loads(requests.get("%s/post/index.json?limit=%d&tags=%s" % (base, limit, urllib.quote(tags))).content)


def get_by_id(id):
    """
    Download an image by ID
    """
    return json.loads(requests.get("%s/post/show.json?id=%d" % (base, id)).content)