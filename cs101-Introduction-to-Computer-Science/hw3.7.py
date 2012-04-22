#!/usr/bin/python2.6

#The web crawler we built at the
#end of Unit 2 has some serious
#flaws if we were going to use
#it in a real crawler. One
#problem is if we start with
#a good seed page, it might
#run for an extremely long
#time (even forever, since the
#number of URLS on the web is not
#actually finite). The final two
#questions of the homework ask
#you to explore two different ways
#to limit the pages that it can
#crawl.


#######

#TWO GOLD STARS#

#Modify the crawl_web procedure
#to take a second parameter,
#max_depth, that limits the
#minimum number of consecutive
#links that would need to be followed
#from the seed page to reach this
#page. For example, if max_depth
#is 0, the only page that should
#be crawled is the seed page.
#If max_depth is 1, the pages
#that should be crawled are the
#seed page and every page that links
#to it directly. If max_depth is 2,
#the crawl should also include all pages
#that are linked to by these pages.


#The following definition of
#get_page provides an interface
#to the website found at
#http://www.udacity.com/cs101x/index.html

#The function output order does not affect grading.

#crawl_web("http://www.udacity.com/cs101x/index.html",0) => ['http://www.udacity.com/cs101x/index.html']
#crawl_web("http://www.udacity.com/cs101x/index.html",1) => ['http://www.udacity.com/cs101x/index.html', 'http://www.udacity.com/cs101x/flying.html', 'http://www.udacity.com/cs101x/walking.html', 'http://www.udacity.com/cs101x/crawling.html']
#crawl_web("http://www.udacity.com/cs101x/index.html",50) => ['http://www.udacity.com/cs101x/index.html', 'http://www.udacity.com/cs101x/flying.html', 'http://www.udacity.com/cs101x/walking.html', 'http://www.udacity.com/cs101x/crawling.html', 'http://www.udacity.com/cs101x/kicking.html']


def sim_get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return  '<html> <body> This is a test page for learning to crawl! <p> It is a good idea to  <a href="http://www.udacity.com/cs101x/crawling.html">learn to crawl</a> before you try to  <a href="http://www.udacity.com/cs101x/walking.html">walk</a> or  <a href="http://www.udacity.com/cs101x/flying.html">fly</a>. </p> </body> </html> '
        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return  '<html> <body> I have not learned to crawl yet, but I am quite good at  <a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>. </body> </html>'
        elif url == "http://www.udacity.com/cs101x/walking.html":
            return '<html> <body> I cant get enough  <a href="http://www.udacity.com/cs101x/index.html">crawling</a>! </body> </html>'
        elif url == "http://www.udacity.com/cs101x/flying.html":
            return '<html> <body> The magic words are Squeamish Ossifrage! </body> </html>'
    except:
        return ""
    return ""

import urllib
def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


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

def crawl_web(seed,max_depth,max_links=1e6):
    tocrawl = [seed]
    crawled = []
    depthtocrawl = [0]*len(tocrawl)
    depth = 0
    page = tocrawl.pop()
    depth = depthtocrawl.pop()
    links = 0
    while depth<=max_depth and links<max_links:
        links += 1
        if page not in crawled:
            i0=len(tocrawl)
            union(tocrawl, get_all_links(get_page(page)))
            crawled.append(page)
            for i in range(i0,len(tocrawl)):
                depthtocrawl.append(depth+1)
        if not tocrawl: break
        page = tocrawl.pop(0) # FIFO to insure breadth first search
        depth = depthtocrawl.pop(0) # FIFO
    return crawled

#print crawl_web("http://www.udacity.com/cs101x/index.html",0)
#print set(crawl_web("http://www.udacity.com/cs101x/index.html",0)) == set(['http://www.udacity.com/cs101x/index.html'])
#print crawl_web("http://www.udacity.com/cs101x/index.html",1)
#print set(crawl_web("http://www.udacity.com/cs101x/index.html",1)) == set(['http://www.udacity.com/cs101x/index.html', 'http://www.udacity.com/cs101x/flying.html', 'http://www.udacity.com/cs101x/walking.html', 'http://www.udacity.com/cs101x/crawling.html'])
#print crawl_web("http://www.udacity.com/cs101x/index.html",50)
#print set(crawl_web("http://www.udacity.com/cs101x/index.html",50)) == set(['http://www.udacity.com/cs101x/index.html', 'http://www.udacity.com/cs101x/flying.html', 'http://www.udacity.com/cs101x/walking.html', 'http://www.udacity.com/cs101x/crawling.html', 'http://www.udacity.com/cs101x/kicking.html'])

