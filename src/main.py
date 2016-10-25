#!/usr/bin/env python

from twitter import Twitter, OAuth
from processing import process_post
from threading import Timer
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

    Timer(600, run).start()


run()