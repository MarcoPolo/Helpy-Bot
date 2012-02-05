import sys
import random
import urllib
import reddit
import tweepy
import subprocess
import json
import re
from tweepy.streaming import StreamListener, Stream
from wordnik import Wordnik
import json

w = Wordnik(api_key="58472987eaefce26a73060d591106e49a79b3f586c0d3150a")

class HelpyBot(StreamListener):
    def __init__(self, api):
        self.commands = ['insult', 'compliment', 'isup', 'reminder','download','music', 'funnypic', 'define', 'kittenme']
        self.api = api
        super(HelpyBot, self).__init__()

    def on_error(self, status_code):
        print '[Helpy] Error - status code = %s' % status_code
        return True

    def on_timeout(self):
        return True

    # Parses the given status, and routes it to a command.
    def on_status(self, status):
        tweet = self.parse_status(status, {})#status.text)

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
        #parsed['sender'] = status.user.screen_name
        return parsed

    # Post text as a tweet to Helpy's account. 
    def post_tweet(self, text):
        print text #todo: make it post tweets to helpy_bot's account

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
        user = 'dr_choc'
        #user = tweet['sender']
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
        user = 'dr_choc'
        #user = tweet['sender']
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
        user = 'dr_choc'
        #user = tweet['sender']

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

if __name__ == '__main__':

    # Setup API credentials.
    from secretStuff import *
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Setup Helpy to listen to twitter stream.
    helpy = HelpyBot(api)
    #helpy.on_status('@Helpy_bot insult @thompson if you would be so kind.')
    #helpy.on_status('@Helpy_bot compliment @ronald if you would be so kind.')
    #helpy.on_status('@Helpy_bot isup google.com')
    #helpy.on_status('@Helpy_bot isup http://www.google.com')
    #helpy.on_status('@Helpy_bot download http://www.google.com lol.txt')
    helpy.on_status('@Helpy_bot define beef')
    helpy.on_status('@Helpy_bot isup http://www.google.com')
    helpy.on_status('@Helpy_bot music')
    helpy.on_status('@Helpy_bot kittenme')
    #helpy.on_status('@Helpy_bot reminder in 0:01 to blah blah blah poop')

    #listener = HelpyBot()
    #stream = Stream(auth, listener)
    #stream.filter(follow=(483102366,),)

