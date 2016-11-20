#!/usr/bin/env python3

import dblink
import random

def proposeStarterArticles(dbconn, uid):
    random_starters = [random.randint(0, 3), random.randint(0, 3)]
    
    articles_low = dblink.getArticlesWithScoreBounds(dbconn, random_starters[0], random_starters[0])
    articles_high = dblink.getArticlesWithScoreBounds(dbconn, random_starters[1], random_starters[1])
    
    # pick one at random and register it
    proposedArticles = [articles_low[random.randint(0, len(articles_low)-1)], articles_high[random.randint(0, len(articles_high)-1)]]
    
    # swap if random
    swapA = random.randint(0, 1)
    swapB = random.randint(0, 1)
    proposedArticles[swapA], proposedArticles[swapB] = proposedArticles[swapB], proposedArticles[swapA]
    
    dblink.setProposedEntries(dbconn, uid, [a["num"] for a in proposedArticles])
    return proposedArticles
    

def proposeTwoArticles(dbconn, uid, prevScore):
    ids = [ int(float(prevScore)), (int(float(prevScore)) + 2) % 4 ]
    
    articles_low = dblink.getArticlesWithScoreBounds(dbconn, ids[0], ids[0])
    articles_high = dblink.getArticlesWithScoreBounds(dbconn, ids[1], ids[1])
    
    # pick one at random and register it
    proposedArticles = [articles_low[random.randint(0, len(articles_low)-1)], articles_high[random.randint(0, len(articles_high)-1)]]
    
    # swap if random
    swapA = random.randint(0, 1)
    swapB = random.randint(0, 1)
    proposedArticles[swapA], proposedArticles[swapB] = proposedArticles[swapB], proposedArticles[swapA]
    
    dblink.setProposedEntries(dbconn, uid, [a["num"] for a in proposedArticles])
    return proposedArticles

def registerUserVote(dbconn, uid, articleID):
    if len(dblink.getUserVotes(dbconn, uid)) < 5:
        proposedOnes = dblink.getProposedEntries(dbconn, uid)
        if not articleID in proposedOnes:
            print("<div class=\"error\">Article " + str(articleID) + " wasn't in the proposed ones!</div>")
        else:
            articleScore = dblink.getArticleInfo(dbconn, articleID)["score"]
            dblink.castVote(dbconn, uid, articleScore)
    
def conclude(dbconn, uid):
    # for the moment we just computer the average
    votes = [float(i) for i in dblink.getUserVotes(dbconn, uid)]
    v_avg = sum(votes) / len(votes)
    print("<h3>Your vote scores are : " + ",".join([str(int(v)) for v in votes]) + "</h3>")
    print("<h4>The meaning of these scores are : 0 is for an article speaking of the Democrat party with a negative sentiment, \
        1 for the same party with a positive sentiment, 2 for the Republican party with a positive sentiment and 3 for the \
        Republican party with a negative sentiment.</h4>")
    # Check for the absence of major deviations (>= 0.5)
    voted = [False, False, False, False]
    for v in votes:
        voted[int(v)] = True
    
    # find crosses 
    nodev = (voted[0] and voted[2]) or (voted[1] and voted[3])
    
    if nodev:
        print("<h2>You seem to be victim of an echo chamber...</h2>")
    else:
        print("<h2>You seem to consider multiple opinion lines!</h2>")
