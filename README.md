# anagrammm
A python bot that crawls reddit and finds anagram comments. The heart of /u/anagrammm.

## Dependencies

ana.py requires the following nonstandard python modules:

```
requests
json
unidecode
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

this will connect to the list of subreddits in sublist.py and will crawl them for comments. After each sub is finished, ana.py will download the current database to the file 'data' in the project folder. This file is overwritten, so any data from previous runs will be lost.

This command takes **a lot** of time. Run it overnight.

### Finding anagrams (quick)

You can find anagrams even while ana.doit() is working, using data from subreddits crawled up to that point. (Just wait for at least a few subs, as matches from the same sub are not considered.)

Run

```
python ./readncalc.py
```

this loads up the 'data' file, prints the number of comments in the database, and searches for anagrams, printing them in the process. Information printed includes:

- Subreddits and authors of the comments
- The raw comment bodies
- A "permstring" (something like "anagrammm:I:love:"), you can safely ignore this
- Direct permalink URLs

### Finding anagrams (nicer)

Fire up the python shell and import ana.py and cPickle:

```python
>>> import ana
>>> import cPickle as pickle
```

then load 'data':

```python
>>> db = pickle.load(open('data','r'))
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

and this will do the same as readncalc.py, and will display the same information. However, when it's done, db will now have the .anagrams attribute:

```python
>>> len(db.anagrams)
528
```

this is a list of candidate anagram groups, which in turn are lists of comments that are anagrams of eachother. This is all the information you need. For example, you can sort by length:

```python
>>> db.anagrams.sort(key = lambda a : len(a[0].clean))
>>> db[:100]
```

and so on.

