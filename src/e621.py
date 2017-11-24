import json
import urllib

import requests

base = 'https://e621.net'
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.04 Chromium/11.0.696.0 Chrome/11.0.696.0 Safari/534.24."}


def get_latest(tags="", limit=1):
    """
    Get the latest image(s) with these filters
    """
    url = "%s/post/index.json?limit=%d&tags=%s" % (base, limit, urllib.quote(tags))
    return json.loads(requests.get(url, headers=headers).content)


def get_by_id(id):
    """
    Download an image by ID
    """
    url = "%s/post/show.json?id=%d" % (base, id)
    return json.loads(requests.get(url, headers=headers).content)
