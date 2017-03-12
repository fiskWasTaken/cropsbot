#!/usr/bin/env python

from threading import Timer

import yaml
import random
from twitter import Twitter, OAuth

import e621

config = yaml.load(open('config.yml'))


def get_a_crop():
    from processing import process_post
    posts = e621.get_latest(tags=config['tags'], limit=config['pool_size'])

    for post in posts:
        result = process_post(post)

        if result is not None:
            return post, result

    return None, None


def get_media_twitter():
    return Twitter(auth=OAuth(**config['twitter']['media']))


def get_meta_twitter():
    return Twitter(auth=OAuth(**config['twitter']['meta']))


def get_artist_name(post):
    """
    gets a nicely formatted artist name for the post
    """
    if len(post['artist']) == 0:
        return "unknown artist"

    return post['artist'][0].replace("_(artist)", "")


def get_tags_string(post, length=3):
    """
    splits the tags string into an actual array, shuffles it and picks the first few
    """
    tags = list(map(lambda tag: '#' + tag, post['tags'].split(' ')))
    random.shuffle(tags)
    return " ".join(tags[:length])


def post_to_twitter(post, result):
    import cv2
    cv2.imwrite('out/%d.jpg' % int(post['id']), result)
    cv2.imwrite("out/last.jpg", result)

    t_upload = Twitter(domain='upload.twitter.com', auth=OAuth(**config['twitter']['media']))

    with open("out/last.jpg") as imagefile:
        imagedata = imagefile.read()

    id_img = t_upload.media.upload(media=imagedata)["media_id_string"]
    media_tweet = get_media_twitter().statuses.update(status="", media_ids=",".join([id_img]))

    print("Posted %d.jpg" % int(post['id']))

    artist_name = get_artist_name(post)
    tags_string = get_tags_string(post)

    status = "https://e621.net/post/show/%d (%s) [%s]" % (post['id'], artist_name, tags_string)

    get_meta_twitter().statuses.update(status=status, in_reply_to_status_id=media_tweet['id'])

    print("Posted metadata")


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
