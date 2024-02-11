from django import template

register = template.Library()


@register.simple_tag()
def get_filters(number, name, encode=None):
    url = '?{}={}'.format(name, number)
    if encode:
        quary = encode.split("&")
        quary_filter = filter(lambda x: x.split('=')[0] != name, quary)
        join = "&".join(quary_filter)
        url = '{}&{}'.format(url, join)
    return url
