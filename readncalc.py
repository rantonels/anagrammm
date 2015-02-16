import ana
import cPickle as pi

print "loading database..."
db = ana.load_crawld()

print "loaded %d comments."%len(db.data)

print "finding anagrams..."
db.find_anagrams(verbose = False)

pi.dump(db.anagrams,open('anagrams','w'))
