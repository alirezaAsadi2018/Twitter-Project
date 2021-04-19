import re
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

def create_hashtag_link(tag):
    url = "/tags/{}/".format(tag)
    # or: url = reverse("hashtag", args=(tag,))
    return '<a href="{}">#{}</a>'.format(url, tag)


@register.filter(name='hashtolink')
def hashtag_links(value):
    return mark_safe(
        re.sub(r"#(\w+)", lambda m: create_hashtag_link(m.group(1)),
               escape(value)))