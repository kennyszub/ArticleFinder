#!/usr/bin/python

import sys
from Monitor import Monitor
from Story import Story

# Add website url sources here - must be full url
SOURCES = ["http://cnn.com", "http://bbc.com", "http://boston.com",
           "http://nytimes.com", "http://huffingtonpost.com"]

def main():
    """Main function that takes initial user input"""
    print "Welcome! This program's purpose is to find links to articles relevant to"
    print "topics that are interesting to you - from many different sources.\n" 
    print "You may also query the database for articles you've previously found.\n"

    monitor = Monitor()

    while(True):
        print "Type 'find' to find new articles online from popular news sources."
        print "Type 'query' to search the database for old articles."
        mode = raw_input()
        if (mode == "find"):
            findMode(monitor) 
        elif (mode == "query"):
            queryMode(monitor)
        else:
            continue

def findMode(monitor):
    """Controls the flow of finding articles and updating the database"""
    while(True):
        print "Enter key words to search for separated by a comma:"
        keyWords = raw_input()
        if (keyWords == ""):
            continue
        keyWords = [w.strip() for w in keyWords.split(",")]
        print "Searching for articles related to those keywords..."
               
        for source in SOURCES:
            links = monitor.scrapeURL(source, keyWords) 
            print("Found %d article(s) on %s\n" % (len(links), source))
            for link in links:
                title = link.string
                url = link.get("href")
                story = Story(title, url, keyWords, source)
                doc = story.getDocument()  

                # Insert document into database
                monitor.addToDatabase(doc)

                # Print results to console
                print "ARTICLE TITLE: %s" % title
                print "URL: %s" % url
        break

def queryMode(monitor):
    """Controls the flow of querying the database for previous articles"""
    while(True):
        print "Type 'topic' to search the database for topics."
        print "Type 'date' to search the database by date."
        queryType = raw_input()

        if (queryType == "topic"):
            print "Enter key words to search database for separated by a comma:"
            keyWords = raw_input()
            if (keyWords == ""):
                continue
            keyWords = [w.strip() for w in keyWords.split(",")]
            monitor.findArticlesOnTopics(keyWords)

        elif (queryType == "date"):
            print "Enter a date in YYYY-MM-DD format - this will search the database for articles added after that date:"
            date = raw_input()
            monitor.findArticlesAfterDate(date)
        else:
            continue

        break
            

# Begin program
if __name__=="__main__":
    main()
