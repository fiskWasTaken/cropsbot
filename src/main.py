#!/usr/bin/env python

from twitter import Twitter, OAuth
from processing import process_post
import yaml
import e621
import cv2


config = yaml.load(open('config.yml'))


def get_a_crop():
    posts = e621.get_latest(tags="rating:e -swf -webm -gif order:random score:>5", limit=10)
    # posts = [e621.get_by_id(1030454)]

    for post in posts:
        result = process_post(post)

        if result is not None:
            return post, result


def get_oauth_bundle(conf):
    return OAuth(conf['access_token_key'], conf['access_token_secret'], conf['consumer_key'], conf['consumer_secret'])


post, result = get_a_crop()

if result is None:
    exit()

cv2.imwrite('out/%d.jpg' % int(post['id']), result)

t = Twitter(auth=get_oauth_bundle(config['twitter']))

cv2.imwrite("out/last.jpg", result)

with open("out/last.jpg") as imagefile:
    imagedata = imagefile.read()

# - then upload medias one by one on Twitter's dedicated server
#   and collect each one's id:
t_upload = Twitter(domain='upload.twitter.com', auth=get_oauth_bundle(config['twitter']))

id_img = t_upload.media.upload(media=imagedata)["media_id_string"]
# - finally send your tweet with the list of media ids:
t.statuses.update(status="", media_ids=",".join([id_img]))