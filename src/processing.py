import requests
import openface
import cv2
import yaml
import numpy as np


config = yaml.load(open('config.yml'))
align = openface.AlignDlib(config['dlib_face_predictor'])


def process_post(post):
    print("Sampling %d (%s)" % (post['id'], post['file_url']))

    img = requests.get(post['sample_url']).content
    sample = cv2.imdecode(np.fromstring(img, dtype='uint8'), cv2.CV_LOAD_IMAGE_COLOR)

    if sample is None:
        return None

    print("Original size: {}".format(sample.shape))

    bb, found_size = find_first_face(sample)

    if bb is None:
        print("No match for this image.")
        return None

    img = requests.get(post['file_url']).content
    source = cv2.imdecode(np.fromstring(img, dtype='uint8'), cv2.CV_LOAD_IMAGE_COLOR)

    ratio = max(source.shape[0], source.shape[1]) / float(found_size)

    x1 = int(bb.left() * ratio)
    y1 = int(bb.top() * ratio)
    x2 = int(bb.right() * ratio)
    y2 = int(bb.bottom() * ratio)

    return source[y1:y2, x1:x2]


def find_first_face(source):
    for max_dim in range(200, 800, 40):
        # resize to max_dim
        if source.shape[1] > source.shape[0]:
            dsize = (max_dim, int(source.shape[0] * (max_dim / float(source.shape[1]))))
        else:
            dsize = (int(source.shape[1] * (max_dim / float(source.shape[0]))), max_dim)

        img = cv2.resize(source, dsize)
        img = cv2.copyMakeBorder(img, 0, max_dim - img.shape[0], 0, max_dim - img.shape[1], cv2.BORDER_CONSTANT)

        # `img` is a numpy matrix containing the RGB pixels of the image.
        bb = align.getLargestFaceBoundingBox(img)

        if bb is None:
            # print("Could not find a face bounding box")
            continue

        print("Match found (%s) at sample size (%d, %d)... " % (bb, dsize[0], dsize[1]))

        return bb, max_dim

    return None, None
