#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Geekman2
#
# Created:     15/01/2014
# Copyright:   (c) Geekman2 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib
import cPickle
import time
import smtplib
import string
import cProfile
import datetime

dirs = "C:/Users/Geekman2/Documents/GitHub/Search Engine/"
Fandom = 'LOZ'
print "test"

crawled = []
index = {}

def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('href="/s')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = "https://www.fanfiction.net"+page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_text(page): #Takes the HTML text of a fanfiction as input
    start = page.find("id='storytext'") #finds the story text on that page
    end = page.find('div',start +1)#Finds the end of the story text
    pagetext = page[start+14:end-3] #creates a string of the story text
    return pagetext #Returns the story text

def cleanup(pagetext):
    #Replaces unwanted characters defined in the string 'specials' with whitespace and returns the cleaned text
    specials = '<>"-,()'
    trans = string.maketrans(specials, ' '*len(specials))
    pagetext = pagetext.translate(trans)
    return pagetext

def make_list(cleanedtext):#Takes text as input
    wordlist=[]
    for i in cleanedtext.split():#Split the text at whitespace and begin iterating over them
        wordlist.append(i)
    wordlist = list(set(wordlist))
    return wordlist#return list of unique words in the document

def add_to_index(keyword,url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]

def crawl_web(seed):
    seedpage = "https://www.fanfiction.net/game/Legend-of-Zelda/?&srt=1&r=103&p="+str(seed)
    tocrawl = [seedpage]
    global crawled
    while tocrawl:
        page = tocrawl.pop(0)
        print page
        pagecontent = get_page(page)
        if page not in set(crawled):
            tocrawl.extend(get_all_links(pagecontent))
            uniquewords = make_list(cleanup(get_text(pagecontent)))
            for word in uniquewords:
                add_to_index(word,page)
            crawled.append(page)
    cPickle.dump(crawled,open(dirs+Fandom+"crawled.p","wb"))
    cPickle.dump(index,open(dirs+Fandom+"index.p",'wb'))

def get_info():
    return index,crawled
