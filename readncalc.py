import ana
import cPickle as pi


print "loading database..."
db = pi.load(open('data','r'))

print "loaded %d comments."%len(db.data)

print "finding anagrams..."
db.find_anagrams(verbose = True)

pi.dump(open('anagrams','w'),db.anagrams)
