#!/usr/bin/env python3

import os
import cgi, cgitb 
import dblink
import sqlite3
import propose
import uuid
from http import cookies
import random
import time

random.seed(time.time())

dbconn = dblink.openDbConn()

def outputArticle(article, width):
    print("<div class=\"col-md-" + str(width) + " news_article\"> \
        <div class=\"news_article_title\">")
    print("<a href=\"" + str(article["url"]) + "\" target=\"_blank\">")
    print(article["title"])
    print("</a>")
    print("</div>")
    # If the article has no picture, no problem
    try:
        print("<center><img src=\"" + str(article["image_url"]) + "\" alt=\"Article image\" style=\"max-width: 75%;\"/></center>")
    except:
        print("<center>No image</center>")
        pass
    print("<div class=\"articleTextHolder\">" + article["body_start"] + "</div>")
    print("</div>")

def outputArticleButton(article, width):
    print("<a href=\"?articleID=" + str(article["num"]) + "\">")
    print("<div class=\"col-md-" + str(width) + " voteThisOne\"> This one! </div>")
    print("</a>")
    
def main():
    headers = "Content-Type: text/html\n"
    cookie = cookies.SimpleCookie()
    uid = uuid.uuid4().int & (1<<64)-1
    formValues = cgi.FieldStorage()
    reset_sess = False
    
    try:
        if formValues["reset"] != None:
            reset_sess = True
    except: pass
        
    if reset_sess and 'HTTP_COOKIE' in os.environ:
        cookie_string=os.environ.get('HTTP_COOKIE')
        cookie.load(cookie_string)
        try:
            old_uid = int(cookie["session"].value)
            dblink.removeUserEntry(dbconn, old_uid)
        except: pass
        cookie["session"] = str(uid)
        headers += str(cookie) + "\n"
    elif 'HTTP_COOKIE' in os.environ:
        cookie_string=os.environ.get('HTTP_COOKIE')
        cookie.load(cookie_string)
        try:
            uid = int(cookie["session"].value)
        except:
            cookie["session"] = str(uid)
            headers += str(cookie) + "\n"
    else:
        cookie["session"] = str(uid)
        headers += str(cookie) + "\n"
    
    print(headers)
    before_code = open("./html_open")
    print(before_code.read())
    
    
    try:
        if formValues["articleID"] != None:
            propose.registerUserVote(dbconn, uid, formValues["articleID"].value)
    except KeyError as e:
        pass
    
    votesSoFar = dblink.getUserVotes(dbconn, uid)
    currentlyCastedVotes = len(votesSoFar)
    if currentlyCastedVotes == 5:
        # voting is over !
        propose.conclude(dbconn, uid)
        
    else:
        articles = []
        articleWidth = 4
        print("<h3>Among the following newspaper articles, which one has your preference?</h3>")
        print("<div class=\"container-fluid\"> \
        <div class=\"row\">")
        if currentlyCastedVotes == 0:
            articleWidth = 6
            articles = propose.proposeStarterArticles(dbconn, uid)
        else:
            articleWidth = 6
            articles = propose.proposeTwoArticles(dbconn, uid, votesSoFar[len(votesSoFar) - 1])
        
        for a in articles:
            outputArticle(a, articleWidth)
        print("</div></div>")
        
        print("<div class=\"container-fluid\"> \
        <div class=\"row\">")
        
        for a in articles:
            outputArticleButton(a, articleWidth)
            
        print("</div></div>")
    
    print("<a href=\"?reset=1\"><div class=\"container-fluid\"> \
        <div class=\"row\"> \
        <div class=\"col-md-12 voteThisOne\">Start over</div> \
        </div></div></a>")
    
        
    after_code = open("./html_close")
    print(after_code.read())

main()
    
dblink.terminateConnection(dbconn)
