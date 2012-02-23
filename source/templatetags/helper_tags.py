import re

from django import template


register = template.Library()


@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return ' class = "on"'
    return ''


@register.simple_tag
def external_link(url, text=""):
    text = url.replace('http://', '').replace('https://', '')\
                   .replace('www.', '') if text == "" else text
    if url.find('http') < 0:
        url = 'http://' + url
    return "<a href=\"%s\" title=\"%s\">%s</a>" % (url, text, text)


@register.simple_tag
def email_link(email):
    parts = email.rsplit('.', 1)
    dom = parts.pop()
    email = parts[0].replace('@', '/')
    return "<span class='e'>%s//%s</span>" % (email, dom)
