sublist = [
            'funny',
            'adviceanimals',
            'pics',
            #'aww',             #disallowed
            'blackpeopletwitter',
            'todayilearned',
            #'wtf',             #banned us
            'gifs',
            'videos',
            'gaming',
            'askreddit',
            'leagueoflegends',
            'worldnews',
            'trees',
            'trollxchromosomes',
            'mildlyinteresting',
    #       'pcmasterrace',     #they don't allow links in posts
            'soccer',
            '4chan',
            #'news',            #disallow (also they banned us? Have we even posted here?)
            'showerthoughts',
            'politics',
            'dota2',
            'fatpeoplehate',
            'movies',
            #'nba',             #they flat out banned us
            'pokemon',
            #'science',         #disallow
            'technology',
            'woahdude',         #they love us :)
            'jokes',
            'globaloffensive',
            'tumblrinaction',
            'unexpected',
            'earthporn',
            'iama',
            'atheism',
            'tifu',
            'nottheonion',
            #'reactiongifs',        #cannot post here (banned? Who knows. Inscrutable Reddit burocracy I guess.
                                    # They really could have bothered to write a letter though.)
            'squaredcircle',
            'tumblr',
            'destinythegame',
            'nfl',
            'cats',
            'gentlemanboners',
            'makeupaddiction',
            'celebs',
            'smashbros',
            'interestingasfuck',
            'circlejerk',
            'me_irl',
            'food',
            'cringepics',
            'oddlysatisfying',
            'explainlikeimfive',
            'hockey',
            #'kotakuinaction',      #crosslinking not allowed (Rule 4)
            'games',
            'conspiracy',
            'creepy',
            'wow',
            'tinder',
            'justiceporn',
            'firstworldanarchists',
            'android',
            'hearthstone',
            'skyrim',
            'minecraft',
            'oldschoolcool',
            #'polandball',          #banned us (they ban all bots)
            'relationships',
            'hiphopheads',
            'mildlyinfuriating',
            'writingprompts',
            'coys',
            #'anime',           #they hate bots
            'photoshopbattles',
            'twoxchromosomes',
            'historyporn',
            'roosterteeth',
            #'comics',              #banned
            'youtubehaiku',
            'tf2',
            'teenagers',
            'lifeprotips',
            'bestof',
            'magictcg',
            'starwars',
            'bindingofisaac',
            'india',
            #'askscience',      #disallow
            'thathappened',
            'australia',
            'unexpectedthuglife',
            'ps4',
            'patriots',
            #'trashy',               #they don't like us a lot :/
            'getmotivated',
            'foodporn',
            'childfree',
            #'tattoos',             #not a lot of good comments
            #'shittyreactiongifs',  #relatively few good comments
            'music',
            #'awwnime',             #very few good comments
            'bitcoin',
            'talesfromretail',
            'xboxone',
            'futurology',
            'murica',
            #'fatlogic',            #rule against linking other subs (brigade accusations)
            'podemos',
            'starcraft',
            'facepalm',
            'kerbalspaceprogram',
            'ladyboners',
            'dataisbeautiful',
            'justneckbeardthings',
            'thesimpsons',
            'sneakers',
            'militaryporn',
            'creepypms',
            #'cringe',              #banned us
            'thelastairbender',
            'justrolledintotheshop',
            #'wheredidthesodago',   #banned us
            'nosleep',
            #'talesfromtechsupport', #disallow
            'cosplaygirls',
            'television',
            'shittyaskscience',
            'crappydesign',
            'space',
            'askhistorians',
            'progresspics',
            'art',
            'trollychromosome',
            'gunners',
            'diy',
            'standupshots',
            'quotesporn',
            'electronic_cigarette',
            'redditlaqueristas',
            'cfb',
            '2007scape',
            'punchablefaces',
            'gamegrumps',
            'canada',
            'watchitfortheplot',
            'shittyfoodporn',
            'sweden',
            'mylittlepony',
            'fffffffuuuuuuuuuuuu',
            'animalsbeingjerks',
            'sports',
            'itookapicture',
            'battlestations',
            'europe',
            'gamedeals',
            'h1z1',
            'smite',
            'mapporn',
            'subredditdrama',
            'amiibo',
            'wallpapers',
            'prettygirls',
            'guns',
            'grandtheftautov',
            'runescape',
            'mma',
            'sex',
            'internetisbeautiful',
            'youdontsurf',
            'thewalkingdead',
            'formula1',
            #'carporn',         #a very quiet sub
            #'netflixbestof',   #few good comments
            'fifa'
            #'eyebleach'        #nothing good
            #'woahtube'          #they should like us :)
                                #and maybe they do, but they don't comment.
        ]

def check_sublist_consistency():

    print "sublist has %d subs."%len(sublist)

    if len(set(sublist)) < len(sublist):
        print "sublist has duplicates."
        
        di = None
        dc = {}
        for i in range(len(sublist)):
            if sublist[i] in dc:
                di = i
                break
            else:
                dc[sublist[i]] = 1

        print "one of the duplicates is /r/%s"%sublist[di]
