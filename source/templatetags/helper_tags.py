from random import choice
import re

from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return ' class = "on"'
    return ''


@register.simple_tag
def external_link(url, text=""):
    if url is None:
        return ""

    if text == "":
        for t in ['http://', 'https://', 'www.']:
            text = url.replace(t, '')

    if url[0:4] != "http":
        url = 'http://%s' % url

    # remove a trailing slash if it exists
    if text[-1:] == "/":
        text = text[0:-1]

    return "<a href=\"%s\" title=\"%s\">%s</a>" % (url, text, text)


@register.simple_tag
def email_link(email):
    parts = email.rsplit('.', 1)
    dom = parts.pop()
    email = parts[0].replace('@', '/')
    return "<span class='e'>%s//%s</span>" % (email, dom)


@register.simple_tag
def random_image():
    path = "images/happy"
    images = [
        "1.gif", "2.gif", "3.jpg", "4.gif", "5.gif", "6.jpg", "7.gif",
        "8.jpg", "9.gif", "10.jpg", "11.gif", "12.gif", "13.jpg", "14.gif",
    ]
    return "%s/%s/%s" % (settings.STATIC_URL, path, choice(images))
