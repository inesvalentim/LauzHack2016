#!/usr/bin/env python3

## In this very file, the articles aren't describes by dictionaries. This is basically an abstraction to interact with the database.

import sqlite3

def openDbConn():
    dbconn = sqlite3.connect("app.db")
    dbconn.row_factory = sqlite3.Row
    return dbconn

def castVote(dbconn, uid, vote_score):
    # check if the user already exists...
    existing = dbconn.execute("SELECT `num`, `score_choices` FROM `votes` WHERE `uid` = '" + str(uid) + "'").fetchall() # HACK This is insecure !!
    if len(existing) > 0:
        existingVote = []
        try:
            existingVote = existing[0]["score_choices"].split(",")
        except: pass
        existingVote.append(str(vote_score))
        dbconn.execute("UPDATE `votes` SET `score_choices` = '" + ",".join(existingVote) +"' WHERE `num` = '" + str(existing[0]["num"]) +"'")
        # The user already exists, let's append his vote to the existing votes
    else:
        # The user doesn't exist, thus we insert their uid and vote into the table
        dbconn.execute("INSERT INTO `votes`(`uid`,`score_choices`) VALUES('" + str(uid) + "', '" + str(vote_score) + "')");
    dbconn.commit()

def setProposedEntries(dbconn, uid, entries):
    entry_tab = ",".join([str(e) for e in entries])
    existing = dbconn.execute("SELECT * FROM `votes` WHERE `uid` = '" + str(uid) + "'").fetchall() # HACK This is insecure !!
    if len(existing) == 0:
        # create the user
        dbconn.execute("INSERT INTO `votes`(`uid`) VALUES('" + str(uid) + "')");
    dbconn.execute("UPDATE `votes` SET `proposed_entries` = '" + entry_tab +"' WHERE `uid` = '" + str(uid) +"'")
    dbconn.commit()

def getProposedEntries(dbconn, uid):
    existing = dbconn.execute("SELECT `proposed_entries` FROM `votes` WHERE `uid` = '" + str(uid) + "'").fetchall() # HACK This is insecure !!
    if len(existing) > 0:
        try:
            entries = existing[0]["proposed_entries"].split(",")
            return entries
        except:
            return []
    return []

def removeUserEntry(dbconn, uid):
    dbconn.execute("DELETE FROM `votes` WHERE `uid` = '" + str(uid) + "'") # HACK This is insecure !!
    dbconn.commit()

def getUserVotes(dbconn, uid):
    existing = dbconn.execute("SELECT `num`, `score_choices` FROM `votes` WHERE `uid` = '" + str(uid) + "'").fetchall() # HACK This is insecure !!
    if len(existing) > 0:
        try:
            existingVote = existing[0]["score_choices"].split(",")
            return existingVote
        except:
            return []
    return []

def getArticlesWithScoreBounds(dbconn, lower_bound, upper_bound):
    existing = dbconn.execute("SELECT * FROM `articles` WHERE `score` <= " + str(upper_bound) + " and `score` >= "+ str(lower_bound)).fetchall() # HACK This is insecure !!
    if len(existing) > 0:
        return existing
    return []

def getArticleInfo(dbconn, article_id):
    existing = dbconn.execute("SELECT * FROM `articles` WHERE `num` = " + str(article_id)).fetchall() # HACK This is insecure !!
    if len(existing) > 0:
        return existing[0]
    return []

def terminateConnection(dbconn):
    dbconn.close()
    
