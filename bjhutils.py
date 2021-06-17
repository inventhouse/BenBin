# BJH Utils: Copyright © 2021 Benjamin Holt -- MIT License
# Utilities mostly meant for command-line use in Xonsh

###  URL utils  ###
import urllib.parse as urls

def urlify(**kwargs):
    "URL-encode keyword arguments as a query string"
    return urls.urlencode(kwargs)


def url2d(url):
    "Breaks down a URL into a dictionary, including decoding query string"
    pr = urls.urlparse(url)
    qd = urls.parse_qs(pr.query, keep_blank_values=True)

    unwrap = lambda v: v if type(v) is not list or len(v) != 1 else v[0]  # unwrap single-item lists
    qd = { k: unwrap(v) for k,v in qd.items() }
    pd = pr._asdict()
    pd["query"] = qd
    
    return pd


def d2url(d):
    "Breaks down a URL into a dictionary, including decoding query string"
    if type(d.get("query")) is dict:
        d = d.copy()
        d["query"] = urls.urlencode(d["query"])
    parts = urls.ParseResult(**d)
    return urls.unparse(parts)

#####
