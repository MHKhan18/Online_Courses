# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:Mohammad Khan

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
from pathlib import Path

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
class NewsStory(object):

    def __init__(self,guid,title,description,link,pubdate):
        self.__guid = guid
        self.__title = title
        self.__description = description
        self.__link = link
        self.__pubdate = pubdate
    
    def get_guid(self):
        return self.__guid
    
    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description
    
    def get_link(self):
        return self.__link

    def get_pubdate(self):
        return self.__pubdate




#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):

    def __init__(self,phrase):
        self.__phrase = phrase 

    def is_phrase_in(self,text):
        ''' True if phrase is in text'''

        
        cleaned_text = ""

        for char in text:
            if char in string.punctuation:
                cleaned_text += " "
            else:
                cleaned_text += char 

        pool = cleaned_text.lower().split()

        to_find = self.__phrase.lower().split()
        
        for i in range( len(pool) ) :
            for j in range ( len(to_find) ):
                if i+j >= len(pool):
                    return False
                if to_find[j] != pool[i+j]:
                    break

                if j == len(to_find)-1:
                    return True 
           

        return False 




# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    
    def __init__(self,phrase):
        super().__init__(phrase)
    
    def evaluate(self,story):
        return  self.is_phrase_in(story.get_title())
            
        
        
    


# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    
    def __init__(self,phrase):
        super().__init__(phrase)

    def evaluate(self,story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):

    def __init__(self, time_string):
        self.time = datetime.strptime(time_string, '%d %b %Y %H:%M:%S')
       
        

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):

    def __init__(self,time_string):
        super().__init__(time_string)

    def evaluate(self, story):
        '''fires when a story is published strictly before the trigger’s time'''
        if story.get_pubdate().tzinfo is not None:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
        return story.get_pubdate() < self.time

class AfterTrigger(TimeTrigger):

    def __init__(self,time_string):
        super().__init__(time_string)

    def evaluate(self, story):
        '''fires when a story is published strictly after the trigger’s time'''
        if story.get_pubdate().tzinfo is not None:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
        return story.get_pubdate() > self.time

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):

    def __init__(self,trigger):
        self.__trigger = trigger
    
    def evaluate(self,story):
        return not self.__trigger.evaluate(story)





# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):

    def __init__(self,trigger1,trigger2):
        self.__trigger1 = trigger1
        self.__trigger2 = trigger2
    
    def evaluate(self,story):
        return  self.__trigger1.evaluate(story) and self.__trigger2.evaluate(story)


# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):

    def __init__(self,trigger1,trigger2):
        self.__trigger1 = trigger1
        self.__trigger2 = trigger2
    
    def evaluate(self,story):
        return  self.__trigger1.evaluate(story) or self.__trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    
    result = []
    print ( "there")
    print ( type( triggerlist[0]) )
    for story in stories:
        for trigger in triggerlist:
            print( type( trigger))
            if trigger.evaluate(story):
                result += [story]
    return result
    



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
   
    file_name = str( Path(__file__).resolve().parents[0] /filename) 
    trigger_file = open(file_name, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    
    trigger_file.close()
    
    result = []
    trig_name = {}

    for line in lines:
        content = line.split(",")
        
        if content[0] != "ADD":
            name = content[0]
            trig_type = content[1]
            arg1 = content[2]
            if len(content) > 3:
                arg2 = content[3]
                trig_name[name] = process_trig(trig_type,arg1,arg2) # build up the dictionary
               
            else:
                trig_name[name] = process_trig(trig_type,arg1)
               
        else:
            for i in range( 1,  len(content)):
                result.append( trig_name[ content[i] ] )
        
        return result



def process_trig( trig_type,arg1, arg2 = None ):

    if trig_type == 'TITLE':
        return TitleTrigger(arg1)
    
    if trig_type == "DESCRIPTION":
        return DescriptionTrigger(arg1)
    
    if trig_type == "AFTER":
        return AfterTrigger(arg1)
        
    if trig_type == "BEFORE":
        return BeforeTrigger(arg1)

    if trig_type == "NOT":
        return NotTrigger(arg1)


    if trig_type == "AND":
        return AndTrigger(arg1,arg2)

    if trig_type == "OR":
        return OrTrigger(arg1,arg2)
        

           

           




    



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("CoronaVirus")
        t2 = DescriptionTrigger("economy")
        t3 = DescriptionTrigger("election")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
       
        triggerlist = read_trigger_config( str( Path(__file__).resolve().parents[0] /"triggers.txt") )
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

