import ana
import cPickle as pi

db = pi.load(open('data','r'))

print len(db.data)

db.find_anagrams()
