#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import re
import requests
import json

import unidecode

import cPickle as pickle

import HTMLParser

pattern = re.compile('[\W_]+')
splitpattern = re.compile(r"[\w']+")

htmlparser = HTMLParser.HTMLParser()

#tests = '''Hash functions are used inside some cryptographic algorithms, in digital signatures, message authentication codes, manipulation detection, fingerprints, checksums (message integrity check), hash tables, password storage and much more. As a Python programmer you may need these functions to check for duplicate data or files, to check data integrity when you transmit information over a network, to securely store passwords in databases, or maybe some work related to cryptography.'''


class Word():
    def __init__(self,raw):
        self.raw = raw
        self.clean = pattern.sub('',self.raw).lower()
        self.ordered = ''.join(sorted(self.clean))
        self.ordwordlist = ':'.join(sorted(splitpattern.findall(self.raw.lower())))
        hasher = hashlib.md5(self.ordered)
        self.hashcode = hasher.digest()
        del hasher

    def __repr__(self):
        return "('''"+self.raw+"''', "+self.ordered+", "+self.hashcode+")"

#testw = Word(tests)

REDDIT  = '''http://www.reddit.com/'''
REDDI   = '''http://www.reddit.com'''


mLEN = 6
MLEN = 60
mCOMMENTS = 20

POSTS_PER_SUB = 400

hds = {'User-Agent' : 'a bot that finds anagram comments by /u/rantonels' }

class DB():
    def __init__(self):
        self.data = []
        self.anagrams = []

    def crawl_subr(self,subr):

        orc = len(self.data)

        print
        print "crawling r/"+subr+"..."

        last = ""

        for hundred in range(POSTS_PER_SUB/100):

            print "page %d"%(hundred+1)

            if hundred == 0:
                navigstring = ""
            else:
                navigstring = "&count=%d&after=%s"%(hundred*100,last)

            url = REDDIT + "r/" + subr + "/hot/.json?limit=100" + navigstring

            print "url: "+url
            try:
                r = requests.get(url, headers = hds)
            except requests.exceptions.ConnectionError:
                print "CONNECTION ERROR."
                return


            print "status: "+str(r.status_code)
            
            if (r.status_code != 200):
                print ":( :( :( :("
                return

            rJ = r.json()
            posts = rJ['data']['children']

            last = rJ['data']['after']

            print "found %d posts!"%len(posts)

            counter = 0
            
            ccounter = 0
            
            for p in posts:
                counter+=1
                
                if (p['data']['num_comments'] < mCOMMENTS):
                    print "([%d]: not enough(%d) comments for us!)"%(counter,p['data']['num_comments'])
                    continue

                print "[%d] %s"%(counter,unidecode.unidecode(p['data']['title'])[:40])
        
                

                nurl = REDDIT + p['data']['permalink']+".json?limit=500&showmore=true&depth=30"
                
                try:
                    sr = requests.get(nurl, headers = hds)
                except requests.exceptions.ConnectionError:
                    print "CONNECTION ERROR."
                    continue

                if(sr.status_code != 200):
                    print ":/ :/ :/ :/"
                    continue

                jS = sr.json()

                perma = jS[0]['data']['children'][0]['data']['permalink']
                
                #print "perma prefix: "+perma

                comment_tree = jS[1]['data']['children']

                comments = []

                todo = comment_tree

                while todo:
                    #print len(todo)

                    c = todo.pop()
                    if ('replies' in c['data']) and (c['data']['replies']!=""):
                        toadd = c['data']['replies']['data']['children']
                        todo = todo+toadd
                    comments.append(c)


                #for c in comments:
                #    try:
                #        print "%s|%s: %s"%(c['data']['id'],c['data']['author'],unidecode.unidecode(c['data']['body']))
                #    except KeyError:
                #        print "error with keys :| ?"

                ccounter+=len(comments)

                subcounter = 0

                for c in comments:
                    try:
                        body = htmlparser.unescape(c['data']['body'])
                    except KeyError:
                        #print "keyerror."
                        continue

                    if (len(body) < MLEN) and (len(body) >mLEN):
                            nw = Word(unidecode.unidecode(body))
                            nw.rid = c['data']['id']
                            nw.author = c['data']['author']
                            nw.sub = subr
                            nw.pm = perma + nw.rid
                            self.data.append(nw)
                            subcounter += 1
                                
            print "obtained %d comments (%d kept)"%(len(comments),subcounter)

        print "FINISHED CRAWLING /r/%s! obtained a grand total of %d comments."%(subr, len(self.data)-orc)


    def compute_hashset(self):
        self.hashset = []
        for e in self.data:
            self.hashset.append(e.hashcode)

    def search_candidates(self):
        self.data.sort(key=lambda x: x.ordered)
        self.compute_hashset()

        for i in range(len(self.hashset)-1):
            if (self.hashset[i] == self.hashset[i+1]):
                return (self.hashset[i],i)

        return None
    
    def topfilter(self,w,nan):

        return (
                     #comment must not be the same
                     (not (w.clean in map(lambda x:x.clean,nan)))   and

                     #no comments from the same subs
                     (not (w.sub in map(lambda x:x.sub,nan)))       and

                     #no word permutations!
                     (not (w.ordwordlist in map(lambda x:x.ordwordlist,nan)))

                                )



    def find_anagrams(self):

        #presorting should optimize everything

        self.data.sort(key=lambda x: x.ordered)
        self.compute_hashset()

        i = 0
        while (i < len(self.data)-1):
            #print "processing startmex " + self.data[cc[1]].ordered
            #nan = []
            #todel = []

            if (self.hashset[i] == self.hashset[i+1]):  #start of a matching group
                mstart = i
                while(self.hashset[i] == self.hashset[i+1]):
                    i+=1    #we increment until we're at the last element of the matching group
                #the candidate matching group is mstart:i
               
                nan = self.data[mstart:i+1]
                
                #cleanup on the matching group

               
                #nan = filter(ft,nan)                    

                cc = 0
                while (cc<len(nan)-1):
                    w = nan[cc]
                    rest = nan[cc+1:]

                    if self.topfilter(w,rest):
                        cc+=1
                    else:
                        nan.remove(w)

                #print "%d remaining of %d"%(len(nan),1+i-mstart)

                #save matching group
                if len(nan) > 1:
                            print
                            print "\t%d-element anagram group"%len(nan)
                            print

                            for w in nan:
                                print "[/r/%s]\t%s: %s"%(
                                        w.sub.ljust(16),
                                        unidecode.unidecode(w.author).ljust(20),
                                        unidecode.unidecode(w.raw)
                                            )
                                print w.ordwordlist
                            print
                            for w in nan:
                                print REDDI + (unidecode.unidecode(w.pm))
                            
                            self.anagrams.append(nan)


                
        

            #standard increment
            i+=1



#            for w in self.data[cc[1]:]:
#                if (w.hashcode == cc[0]):                              #check hashes
#                    if not (w.clean in map(lambda x:x.clean,nan)):  #check explicitly if anagram
#                        if not (w.sub in map(lambda x:x.sub,nan)):      #no dupes from the same sub!
#                            nan.append(w)
#                    todel.append(w)               #delete ALL entries that matched the hash
#                else:   #we've reached the end of the matching block
#                    break
#
#            for w in todel:
#                    self.data.remove(w)
#
#
#
#            
#            cc = self.search_candidates()


def doit():

    testdb = DB()

    import sublist

    for sub in sublist.sublist:
        testdb.crawl_subr(sub)


        print "saving %d-entries db..."%len(testdb.data)
        pickle.dump(testdb,open('data','w'))

    testdb.find_anagrams()

