from bot import db, patterns, mentions, monitor
from collections import defaultdict
import feedparser
import re
from stop_words import get_stop_words


stop_words = set(get_stop_words('en'))


def tokenize(fulltext):
    fulltext = re.sub('[^\w]', ' ', fulltext).lower()
    return re.split('\s+', fulltext)


def tokenize_entrydict(entrydict):
    return tokenize(' '.join([entrydict['title'], entrydict['link']]))


def extract_terms(entrydict):
    return set(tokenize_entrydict(entrydict))


def match(terms, e):
    phrase = ' '.join(terms)
    tokens = e.tokens()

    # exact match
    if phrase in ' '.join(tokens):
        return True

    # stopwords match
    if phrase in ' '.join([t for t in tokens if t not in stop_words]):
        return True

    return False


class Entry(object):
    def __init__(self, original, terms, feed_name):
        self.original = original
        self.terms = terms
        self.feed_name = feed_name

    def tokens(self):
        return tokenize_entrydict(self.original)

    def to_mention(self, phrase):
        return {
            'phrase': phrase,
            'feed': self.feed_name,
            'title': self.original['title'],
            'comments_url': self.original['comments'],
            'link_url': self.original['link'],
        }


class InvertedIndex(object):
    def __init__(self, feeds):
        self.feeds = feeds

        # term -> posting list of entries
        self.index = defaultdict(set)

    def build_index(self):
        for name, f in self.feeds.items():
            self.add_feed(name, f)

    def add_feed(self, name, feed):
        for e in feed['entries']:
            terms = extract_terms(e)
            entry = Entry(e, terms, name)

            for t in terms:
                self.index[t].add(entry)

    def search(self, phrase):
        terms = tokenize(phrase)
        postings = None

        # find entries matching all terms in phrase
        for t in terms:
            if not postings:
                postings = self.index[t].copy()
            else:
                postings &= self.index[t]

        if not len(postings):
            return []

        # limit to exact phrases
        for e in postings.copy():
            if not match(terms, e):
                postings.remove(e)

        return [e.to_mention(phrase) for e in postings]


def build_index():
    idx = InvertedIndex({
        'newest': feedparser.parse('http://hnrss.org/newest'),
        'homepage': feedparser.parse('https://news.ycombinator.com/rss'),
    })
    idx.build_index()
    return idx


def run():
    idx = build_index()

    found = 0

    for p in patterns.find_all():
        for mention in idx.search(p['pattern']):
            print('Found mention of "%s" on %s (%s)' % (
                p['pattern'], mention['link_url'], mention['feed']
            ))
            created = mentions.save(p, mention)
            if created:
                found += 1

    if found > 0:
        monitor.notify('Crawler found %s mentions.' % found)
