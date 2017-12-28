import urllib2
from lxml import html
from bs4 import BeautifulSoup
import json
import os

# globals
companiesList = [
    {
        'name' : 'Amazon',
        'link' : 'http://www.geeksforgeeks.org/tag/amazon/page/',
    },
    {
        'name' : 'GoldmanSachs',
        'link' : 'http://www.geeksforgeeks.org/tag/goldman-sachs/page/',
    }
]

def writeToFile(filename, data):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            pass

    with open(filename, "w") as f:
        f.write(str(data))

def GetPageSource(company, page_num):
    pathWithFolders = company['name'] + '//' + 'metaData' + str(page_num)
    #print (pathWithFolders)
    if os.path.exists(pathWithFolders):
        print "offline"
        with open(pathWithFolders, 'r') as f:
            soup = f.read()
            f.close()
        return BeautifulSoup(soup, "lxml")
    else:
        print "online"
        link = company['link'] + str(page_num) + "/"
        print(link)
        try :
            page = urllib2.urlopen(link)
            #print page.getcode()
            #print page
            soup = BeautifulSoup(page, "lxml")
            with open(pathWithFolders, 'w') as f:
                f.write(str(soup))
                f.close()
            return soup
        except urllib2.HTTPError, e:
            print e.getcode()

def ProcessArticle(soup, filename):
    # if not os.path.exists(filename):
    #     with open(filename, 'w') as f:
    #         content = soup.find("div", class_="entry-content")
    #         paragraphs = content.find_all("p")
    #         for p in paragraphs:
    #             f.write(str(p.get_text()))
    #     f.close()
    pass

def CreateArticle(company, url, filename):
    print url
    pathWithFolders = company['name'] + '//RawArticles//' + filename
    #print pathWithFolders
    if os.path.exists(pathWithFolders):
        print "offline article"
    else :
        print "online article"
        try :
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page, "lxml")
            with open(pathWithFolders, 'w') as f:
                f.write(str(soup))
                f.close()
        except :
            raise
    pathWithFolders = company['name'] + '//Articles//' + filename
    ProcessArticle(soup, pathWithFolders)

def GetListOfArticles(soup):
    lists = soup.find_all("article")
    return lists

def GetArticleLink(soup):
    link = soup.find("a")
    return link

try :
    for company in companiesList :
        pageNum = 1
        firstArticle = True
        while True:
            soup = GetPageSource(company, pageNum)
            try :
                listOfArticles = GetListOfArticles(soup)
                #print (len(listOfArticles))
                for article in listOfArticles:
                    articleLink = GetArticleLink(article)
                    #print articleLink["href"]
                    print articleLink.get_text()
                    if firstArticle == True:
                        firstArticle = False
                        pathWithFolders = company['name'] + '//' + 'metaData'
                        #print (pathWithFolders)
                        with open(pathWithFolders, 'w') as f:
                            f.write(articleLink.get_text())
                            f.close()
                    CreateArticle(company, articleLink["href"], articleLink.get_text())
                pageNum = pageNum + 1
            except:
                print "Article not found"
                break
except :
    print "Page not found"

for company in companiesList :

    pass