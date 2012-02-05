import sys
import random
import urllib
#import reddit
import tweepy
import subprocess
import json
import re
from tweepy.streaming import StreamListener, Stream
from wordnik import Wordnik
import json

w = Wordnik(api_key="58472987eaefce26a73060d591106e49a79b3f586c0d3150a")

try:
    from xml.etree import ElementTree # for Python 2.5 users
except ImportError:
    from elementtree import ElementTree
import atom.service
import atom
import getopt
import string
import time
import gdata
import gdata.calendar
import gdata.service
import gdata.calendar.service

from secretStuff import *


calendar_service = gdata.calendar.service.CalendarService()
calendar_service.email = email
calendar_service.password = password
calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
calendar_service.ProgrammaticLogin()


class HelpyBot(StreamListener):
    def __init__(self, api):
        self.commands = ['insult', 'compliment', 'isup', 'reminder','download','music', 'funnypic', 'define', 'kittenme', 'flipcoin', 'likeaboss','calendar']
        self.api = api
        super(HelpyBot, self).__init__()

    def on_error(self, status_code):
        print '[Helpy] Error - status code = %s' % status_code
        return True

    def on_timeout(self):
        return True

    # Parses the given status, and routes it to a command.
    def on_status(self, status):
        print 'the status was',status.text
        return
        tweet = self.parse_status(status.text, status)

        if (not re.match('@helpy_bot', tweet['target'])):
            print '[Helpy] Tweet not meant for Helpy Bot.'
            return

        if (tweet['command'] in self.commands):
            getattr(self, tweet['command'])(tweet)
        else:
            print '[Helpy] Error - unknown command %s' % tweet['command']

    # Helper Methods
    # --------------
    # Tokenizes the text status.

    def parse_status(self, text, status):
        tokens = text.lower().split()
        parsed = {}
        parsed['target'] = tokens[0]
        parsed['command'] = tokens[1].strip('.,!?')
        parsed['text'] = tokens[2:]
        parsed['raw_text'] = ' '.join(tokens[2:])
        parsed['sender'] = status.user.screen_name
        return parsed

    # Post text as a tweet to Helpy's account. 
    def post_tweet(self, text):
        self.api.update_status('howdysasd asjdkajsdkj alksjd')

    # Command Implementations
    # -----------------------

    def insult(self, tweet):
        insults = open('insults.txt').read().split('\n')
        text = tweet['text']
        target = text[0]
        response = ''

        while (response == '' or len(response) > 140):
            response = '%s %s' % (target, insults[random.randint(0,96)])
        self.post_tweet(response)
    
    def compliment(self, tweet):
        compliments = open('compliments.txt').read().split('\n')
        text = tweet['text']
        target = text[0]
        response = ''

        while (response == '' or len(response) > 140):
            response = '%s %s' % (target, compliments[random.randint(0,45)])
        self.post_tweet(response)

    def download(self, tweet):
        text = tweet['text']
        url = text[0]
        if (url.find('http://') == -1 and url.find('https://') == -1 ):
            url = 'http://'+url
        try:
            name = text[1]
        except:
            name = "potato"
        if (name.find('.') == -1):
            fileExt = url.split('/')[-1]
            fileExt = fileExt[:fileExt.find('.')]
        else:
            fileExt = ''

        # feeble attempt to protect against shell injection
        if(fileExt == '.torrent'):
            fileExt = fileExt.replace(';','')
            fileExt = fileExt.replace("'",'')
            subprocess.call("deluge-console add '"+url+"'")
        else:
            urllib.urlretrieve (url, name+fileExt)
        
    def isup(self, tweet):
        text = tweet['text']
        url = text[0]
        if (url.find('http://') == -1 and url.find('https://') == -1 ):
            url = 'http://'+url
        user = tweet['sender']
        up = False

        try:
            returnCode = urllib.urlopen(url).getcode()
            if returnCode == 200:
                up = True
        except: pass

        response = '@%s, seems to be %s from here!' % (user, 'up' if up else 'down')
        self.post_tweet(response)

    def music(self, tweet):
        music = urllib.urlopen('http://hypem.com/playlist/latest/fresh/json/1/data.js')
        music = music.read()
        music = json.loads(music)
        song = music[str(random.randint(0,len(music)))]
        url = urllib.quote(song["title"])
        response = 'http://grooveshark.com/#!/search?q='+url
        self.post_tweet(response)

    def reminder(self, tweet):
        text = tweet['text']
        user = tweet['sender']
        time = text[1].split(':')
        reminder = text[3:]
        reminder = ' '.join(reminder)
        reminder = reminder.replace(';','')
        reminder = reminder.replace('\'','')

        # get hours and minutes from 'time' and create a readable 'time_text'
        # for when the reminder will be executed.
        import datetime
        hours = int(time[0])
        minutes = int(time[1])
        seconds = (hours * 60 * 60) + (minutes * 60)
        now = datetime.datetime.now()
        later = now + datetime.timedelta(0, seconds)
        time_text = later.strftime('%I:%M %p')

        response = '@%s, I set a reminder for %s.' % (user, time_text)
        procs = subprocess.Popen('sleep '+str(seconds)+"; python post.py '"+ reminder+"'", shell=True)
        self.post_tweet(response)

    def funnypic(self, tweet):
        text = tweet['text']
        user = tweet['sender']

        r = reddit.Reddit(user_agent='helpy_bot')
        submissions = r.get_subreddit('funny').get_hot(limit=25)
        image_link = ''
        while (True):
            submission = submissions.next()
            if ('imgur.com' in submission.url):
                image_link = submission.url
                break

        response = '@%s, enjoy: %s' % (user, image_link)
        self.post_tweet(response)
 
    def calendar(self, tweet):
        text = tweet['text']
        data = ' '.join(text)
        event = gdata.calendar.CalendarEventEntry()
        event.content = atom.Content(text=data)
        event.quick_add = gdata.calendar.QuickAdd(value='true')

        new_event = calendar_service.InsertEvent(event, '/calendar/feeds/default/private/full')



    def define(self, tweet):
        from pprint import pprint
        word = tweet['text'][0] # get word to lookup
        url = "http://dictionary.reference.com/browse/"+word
        output = w.word_get_definitions(word)
        #pprint(output)
        if (output == []):
            self.post_tweet("I'm sorry, the word you requested does not exist.")
            return
        a = 0
        response = output[a]
        a = 1
        while (len(response['text']) >= 140):
            if (a >= len(output)):
                self.post_tweet("I'm sorry, all definitions are too long.")
                return
            response = output[a]
            a+=1
        
        self.post_tweet(response['text'])

    def kittenme(self, tweet):
        rand_h = random.randint(300,700)
        rand_w = random.randint(300,700)
        url = "http://placekitten.com/g/"+str(rand_w)+"/"+str(rand_h)
        self.post_tweet(url)

    def flipcoin(self, tweet):
        thecoin = ["Heads", "Tails"]
        self.post_tweet(thecoin[random.randint(0,1)])

    def likeaboss(self, tweet):
        images = [
            "http://s3.amazonaws.com/kym-assets/photos/images/original/000/114/151/14185212UtNF3Va6.gif?1302832919",
            "http://s3.amazonaws.com/kym-assets/photos/images/newsfeed/000/110/885/boss.jpg",
            "http://verydemotivational.files.wordpress.com/2011/06/demotivational-posters-like-a-boss.jpg",
            "http://assets.head-fi.org/b/b3/b3ba6b88_funny-facebook-fails-like-a-boss3.jpg",
            "http://img.anongallery.org/img/6/0/like-a-boss.jpg",
            "http://www.youtube.com/watch?v=NisCkxU544c",
            "http://pigroll.com/img/like_a_boss.jpg",
            "http://3.bp.blogspot.com/-bY9Ca6gmUz4/TrQC_cdBwQI/AAAAAAAACR4/vwDskIZk1k0/s1600/baby+boss.jpg"
        ]
        self.post_tweet(images[random.randint(0, len(images)-1)])

if __name__ == '__main__':

    # Setup API credentials.
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Setup Helpy to listen to twitter stream.
    helpy = HelpyBot(api)
    stream = Stream(auth, helpy)
    stream.filter(follow=(483102366,),)
    #api.update_status('asda asd asd a')

    #helpy.on_status('@Helpy_bot insult @thompson if you would be so kind.')
    #helpy.on_status('@Helpy_bot compliment @ronald if you would be so kind.')
    #helpy.on_status('@Helpy_bot isup google.com')
    #helpy.on_status('@Helpy_bot isup http://www.google.com')
    #helpy.on_status('@Helpy_bot download http://www.google.com lol.txt')
    #helpy.on_status('@Helpy_bot define beef')
    #helpy.on_status('@Helpy_bot isup http://www.google.com')
    #helpy.on_status('@Helpy_bot music')
    #helpy.on_status('@Helpy_bot kittenme')
    #helpy.on_status('@Helpy_bot flipcoin')
    #helpy.on_status('@Helpy_bot reminder in 0:01 to blah blah blah poop')
    #helpy.on_status('@Helpy_bot funnypic, please')
    #helpy.on_status('@Helpy_bot calendar Dentist 7pm-8pm')
    #helpy.on_status('@Helpy_bot likeaboss')


