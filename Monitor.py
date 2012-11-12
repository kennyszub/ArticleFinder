#!/usr/bin/python

from pymongo import Connection
from bs4 import BeautifulSoup
import urllib2
import re

class Monitor:
    """The Monitor class represents the database and the methods to modify/query it.
       It also contains the scraping functionality"""

    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'
    HEADERS = { 'User-Agent' : USER_AGENT }
 
    def __init__(self):
        """Initialize database and stories collection"""
        connection = Connection()
        db = connection.story_database
        self.stories = db.stories

    def scrapeURL(self, url, keyWords):
        """Scrape the given url for article titles with the given keywords.
           Return a list of BeautifulSoup objects"""
        try:
            req = urllib2.Request(url, None, Monitor.HEADERS)
            response = urllib2.urlopen(req)
            page = response.read()
            soup = BeautifulSoup(page, "html5lib")
        except(urllib2.URLError):
            print "ERROR: Could not load %s" % url
            return []
            
        # Construct regex
        regex = "^"
        template = "(?=.*\\b%s\\b)"
        for keyWord in keyWords:
            regex += template % keyWord
        regex = re.compile(r"" + regex, re.IGNORECASE)

        links = soup.find_all('a', text=regex)
        return links

    def addToDatabase(self, document):
        """Add the given document to the stories database"""
        # Performs upsert to prevent duplicates
        self.stories.update(document, document, upsert=True)


    def findArticlesOnTopics(self, topics):
        """Search the stories database for the given topics""" 
        for article in self.stories.find({"keywords": {"$in" : topics}}):
            print "TITLE: %s" % article["title"]
            print "URL: %s\n" % article["url"]

    def findArticlesAfterDate(self, date):
        """Search the stories database for articles after the given date"""
        for article in self.stories.find({"date": {"$gt" : date}}):
            print "TITLE: %s" % article["title"]
            print "URL: %s\n" % article["url"]
        

           

