#!/usr/bin/env python

from threading import Timer

import cv2
import yaml
import random
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

    with Twitter(auth=OAuth(**config['twitter']['media'])) as t:
        t_upload = Twitter(domain='upload.twitter.com', auth=OAuth(**config['twitter']['media']))

        with open("out/last.jpg") as imagefile:
            imagedata = imagefile.read()

        id_img = t_upload.media.upload(media=imagedata)["media_id_string"]
        media_tweet = t.statuses.update(status="", media_ids=",".join([id_img]))

        print("Posted %d.jpg" % int(post['id']))

    with Twitter(auth=OAuth(**config['twitter']['meta'])) as t:
        artist_name = post['artist'].get(0, "unknown artist").replace("_(artist)", "")

        # splits the tags string into an actual array, shuffles it and picks the first few
        tags = map(lambda tag: '#' + tag, post['tags'].split(' '))
        tags = random.shuffle(tags)
        tags_string = " ".join(tags[:3])

        status = "https://e621.net/post/show/%d (%s) [%s]" % (post['id'], artist_name, tags_string)

        t.statuses.update(status=status, in_reply_to_status_id=media_tweet['id'])


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
