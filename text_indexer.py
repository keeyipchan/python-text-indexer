#!/usr/bin/env python

REMOVE_WORDS = [ 'a', 'an', 'and', 'as', 'at', 'before', 'but', 'by', 'for', 'from', 'is', 'in', 'into', 'like', 'of', 'off', 'on', 'onto', 'per', 'since', 'than', 'the', 'this', 'that', 'to', 'up', 'via', 'with', ]

import sys,os,optparse,re,string
from operator import itemgetter
parser = optparse.OptionParser()
parser.add_option('--text', '-s', dest = 'text', help = 'The text to parse keywords from')
parser.add_option('--limit', '-l', dest = 'limit', help = 'The limit of keywords to return. Defaults to returning all keywords.')
parser.add_option('--min-occurrences', '-m', dest = 'min_occurrences', help = 'The number of times a word must occur to be returned')
options,args = parser.parse_args()

if not options.text and len(args):
    options.text  =   args[0]
    
if not options.limit and len(args) > 1:
    options.limit   =   args[1]
    
if not options.min_occurrences and len(args) > 2:
    options.min_occurrences  =   args[2]

def keywords( text, limit = None, min_occurrences = 1 ):
    text        =   text.translate(string.maketrans('', ''), string.punctuation)
    keywords    =   {}
    splitter    =   re.compile( '([\w]+)', re.UNICODE )
    words       =   splitter.findall( re.sub(r'<[^>]*?>', '', text ) )
    for word in words:
        word = word.lower()
        if word in REMOVE_WORDS:
            pass
        elif word in keywords:
            count = keywords[ word ]
            keywords[ word ] = count + 1
        else:
            keywords[ word ] = 1
    keywords = sorted( keywords.items(), key=itemgetter(1), reverse=True )
    def keyword_filter(x):
        return x[1] >= min_occurrences and len(x[0]) > 3
    keywords    =   filter( keyword_filter, keywords )
    keywords    =   [str(x[0]) for x in keywords]
    if limit and len(keywords) > limit:
        keywords    =   keywords[0:limit]
    keywords.sort()
    return list(set(keywords))

def proper_names(text):
    text        =   text.translate(string.maketrans('', ''), string.punctuation)
    name_finder =   re.compile( r'(([A-Z]\.?\w*\-?[A-Z]?\w*)\s?([A-Z]\w*|[A-Z]?\.?)\s?([A-Z]\w*\-?[A-Z]?\w*)(?:,\s|)(Jr\.|Sr\.|IV|III|II|))', re.UNICODE )
    names       =   name_finder.findall( text )
    names       =   [str(x[0]) for x in names]
    names.sort()
        
    return list(set(names))
    
def acronyms(text):
    text        =   text.translate(string.maketrans('', ''), string.punctuation)
    acr_finder  =   re.compile( r'([A-Z]{2:100})', re.UNICODE )
    acrs        =   acr_finder.findall(text)
    acrs.sort()
    return list(set(acrs))

if __name__ == "__main__":
    if not options.text:
        print "You must specify a text to parse"
        sys.exit(os.EX_NOINPUT)
    if options.limit:
        try:
            options.limit   =   int(options.limit)
        except:
            print "You must specify an integer for --limit"
            sys.exit(os.EX_DATAERR)
    else:
        options.limit = None
    if not options.min_occurrences:
        options.min_occurrences = 1
    else:
        try:
            options.min_occurrences = int(options.min_occurrences)
        except:
            print "You must specify an integer for --min-occurrences"
            sys.exit(os.EX_DATAERR)
    words       =   []
    keywords    =   keywords(options.text, limit = options.limit, min_occurrences = options.min_occurrences)
    words       =   words + keywords
    names       =   proper_names(options.text)
    words       =   words + names
    acrs        =   acronyms(options.text)
    words       =   words + acrs
    words       =   list(set(words))
    words.sort()
    print "\n".join([str(x) for x in words])