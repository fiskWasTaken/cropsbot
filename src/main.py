#!/usr/bin/env python

from threading import Timer

import cv2
import yaml
from twitter import Twitter, OAuth

import e621
from processing import process_post

config = yaml.load(open('config.yml'))


def get_a_crop():
    posts = e621.get_latest(tags=config['tags'], limit=config['pool_size'])

    for post in posts:
        result = process_post(post)

        if result is not None:
            return post, result

    return None, None


def post_to_twitter(post, result):
    cv2.imwrite('out/%d.jpg' % int(post['id']), result)
    cv2.imwrite("out/last.jpg", result)

    t = Twitter(auth=OAuth(**config['twitter']))
    t_upload = Twitter(domain='upload.twitter.com', auth=OAuth(**config['twitter']))

    with open("out/last.jpg") as imagefile:
        imagedata = imagefile.read()

    id_img = t_upload.media.upload(media=imagedata)["media_id_string"]
    t.statuses.update(status="", media_ids=",".join([id_img]))

    print("Uploaded %d.jpg" % int(post['id']))


def run():
    try:
        post, result = get_a_crop()

        if post is None:
            print("Could not get a crop")
        else:
            post_to_twitter(post, result)
    except Exception as e:
        print(e)
        print("Continuing run")

    Timer(config['interval'], run).start()


run()
