from urlparse import urlparse


def ui_url(url):
    return urlparse(url).path