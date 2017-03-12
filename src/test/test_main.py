import pytest

from main import get_tags_string, get_artist_name


def test_pick_tags():
    tags = "tagone tagtwo tagthree tagfour"
    assert type(get_tags_string({"tags": tags}, 3)) is str


def test_sanitise_artist_name():
    name1 = "fuck_(artist)"
    assert get_artist_name({"artist": [name1]}) == "fuck"
