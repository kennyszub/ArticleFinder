#!/usr/bin/python

import datetime

class Story:
    """Represents a document object"""

    def __init__(self, title, url, keywords, source):
        """Initialize a story (document)"""
        date = datetime.datetime.now()
        self.date = date.strftime("%Y-%m-%d") 
        self.title = title
        self.url = url
        self.keywords = keywords
        self.source = source

    def getDocument(self):
        """Return a dictionary formatted as a document"""
        story = {"title": self.title,
                 "url": self.url,
                 "keywords": self.keywords,
                 "source": self.source,
                 "date": self.date
                }
        return story
                 


