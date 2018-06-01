from __future__ import with_statement

import feedparser
import contextlib
from urllib.parse import urlencode
from urllib.request import urlopen

# Just some sample keywords to search for in the title
key_words = 'army navy'


def make_tiny(url):
    request_url = ('http://tinyurl.com/api-create.php?' +
                   urlencode({'url':url}))
    with contextlib.closing(urlopen(request_url)) as response:
        return response.read().decode('utf-8')


def contains_wanted(query, in_str):
    query = query.split()
    i = 0
    for wrd in query:
        if wrd.lower() in in_str:
            i += 1
    return i


def search_guides(query):
    rss = 'http://www.nationalarchives.gov.uk/category/records-2/feed/'
    feed = feedparser.parse(rss)
    results = []
    n = 0

    for key in feed["entries"]:
        url = key['link'].replace('livelb', 'www')
        url = make_tiny(url)
        title = key['title']
        content = key['content'][0]['value']
        i = contains_wanted(query, content.lower())

        if i > 0:
            result = '{} - {} - {}'.format(i, title, url)
            print(result)

            row = []
            row.append(i)
            row.append(title)
            row.append(url)
            results.append(row)

            n += 1

    top_result = max(results, key=lambda x: x[0])
    print('{} {}'.format(top_result[1], top_result[2]))

    return '{} {}'.format(top_result[1], top_result[2])



search_guides(key_words)