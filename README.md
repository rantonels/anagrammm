# anagrammm
###[Official reddit thread](https://www.reddit.com/r/botwatch/comments/2vac36/find_recent_comments_that_are_anagrams_of/)

A python bot by [/u/rantonels](https://www.reddit.com/u/rantonels) that crawls reddit and finds anagram comments. The heart of [/u/anagrammm](https://reddit.com/u/anagrammm).

## A word of warning

This repository is only kept for transparency, completeness, convenience, and similar motives. It is not maintained so that it could be easily used by others. Similarly, this documentation is often incomplete, wrong, deceptive and frustrating.

If you want to do the same, you are free to download and inspect the code, but don't expect it to work out of the box. You'd be better off starting from scratch or forking.

## Dependencies

ana.py requires the following nonstandard python modules:

```
requests
json
unidecode
praw
progressbar
```

## System requirements

*this paragraph is only useful to users of embedded systems. Anyone with a normal laptop should have no problems.*

The 'data' file can get pretty big, so make sure you have a GB or two of free disk space.

The scripts are not efficient and will attempt to load all of the database into RAM at the same time. Beware.


## Usage

### Crawling

Enter the python interpreter, and run:

```python
>>> import ana
>>> ana.doit()
```

this will connect to the list of subreddits in sublist.py and will crawl them for comments. After each sub is finished, ana.py will download the current database to the file `crawld/subname`. These files are overwritten, so any data from previous runs will be lost. It is advisable to clear the `crawld/` folder before running `ana.doit()`.

This command takes **a lot** of time. Run it overnight.

### Finding anagrams (quick)

You can find anagrams even while ana.doit() is working, using data from subreddits crawled up to that point. (Just wait for at least a few subs, as matches from the same sub are not considered.)

Run

```
python ./readncalc.py
```

this loads up the `crawld` folder, prints the number of comments in the database, and searches for anagrams, dumping them in the `anagrams` pickled file as a list of `Word()` instances. Editing this line from readncalc.py:

```python
db.find_anagrams(verbose = False)
```

to

```python
db.find_anagrams(verbose = True)
```

makes the anagrams get printed while they're being found, in human readable format. Info printed includes:

- Subreddits and authors of the comments
- The raw comment bodies
- A "permstring" (something like "anagrammm:I:love:"), you can safely ignore this
- Direct permalink URLs

(this is the behaviour of the `ana2string()` function documented below).

### Finding anagrams (nicer)

Fire up the python shell and import ana.py and cPickle:

```python
>>> import ana
```

then load the data:

```python
>>> db = ana.load_crawld()
```

(this should take a little.) Then the .data attribute of db is a list of comment objects:

```python
>>> len(db.data)
(something around 500000)
>>> db.data[0]
('''Something sometging left boob left shark''', abbeeeeffggghhiikllmmnnoooorssstttt, }ے�G�ST���4q�)
```

comments belong to the Word class and have these attributes:

attribute| content
 ------- |-----------------------
.raw      | raw comment string     
.sub      | subreddit they're from 
.clean | only the word characters, in lower case
.ordered | the .clean string, sorted alphabetically
.ordwordlist | a "permstring", basically a list of words, sorted, then ":".joined. Used to exclude word permutations.
.hashcode | a hashed version of .ordered, used for finding anagrams
.rid | the reddit ID of the comment
.author | the username of the author
.pm | the permalink of the comment (missing the "http://reddit.com" prefix)

you can now run

```python
>>> db.find_anagrams()
```

and this will do the same as readncalc.py. (This displays a progress bar, if you want to print directly the anagram groups, do ```db.find_anagrams(verbose=True)```). When it's done, db will now have the .anagrams attribute:

```python
>>> len(db.anagrams)
528
```

this is a list of candidate anagram groups, which in turn are lists of comments that are anagrams of eachother. This is all the information you need. For example, you can sort by length:

```python
>>> db.anagrams.sort(key = lambda a : len(a[0].clean))
>>> top = db[:100]
```

and so on.

An ```ana2string()``` function turns anagram groups into human-readable multiline strings like in the output of ```.find_anagrams(verbose=True)```. For example:

```python
>>> for i in range(100):
>>>    print "# %d"%i
>>>    print ana2string(db[-i])
>>>    print
```

will print the longest 100 anagrams in human readable format.

### Posting

**Do not use this feature if you don't own /u/anagrammm. Your posts using this method will include links to /u/anagrammm and information about him. Do edit the source code to suit your account if you want to post using this feature. Ignore this warning and you will just be giving me and my bot some bizarre publicity.**

Import the ana module and create a Commenter() instance:

```python
import ana
com = ana.Commenter()
```

this will prompt you for reddit username and password.

You can then reply to member comments of an anagram group with:

```python
com.comment_anagram_group(a)
```

where ```a``` is an anagram group, such as an element of ```db.anagrams```.

**Another warning: as of now, this does NOT check if you have already replied to these people. NOR does it check if bots are welcome there. Use with extreme caution. No, wait: when in doubt, don't use.**
