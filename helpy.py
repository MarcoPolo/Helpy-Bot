import sys
import random
import urllib
import tweepy
from tweepy.streaming import StreamListener, Stream

class HelpyBot(StreamListener):
    def __init__(self, api):
        self.commands = ['insult', 'compliment', 'isup', 'reminder','download']
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

        if (tweet['target'] != '@helpy_bot'):
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
        parsed['command'] = tokens[1]
        parsed['text'] = tokens[2:]
        parsed['raw_text'] = ' '.join(tokens[2:])
        #parsed['sender'] = status.user.screen_name
        return parsed

    # Post text as a tweet to Helpy's account. 
    def post_tweet(self, text):
        print text

    # Command Implementations
    # -----------------------

    def insult(self, tweet):
        insults = open('insults.txt').read().split('\n')
        text = tweet['text']
        user = text[0]
        response = ''

        while (response == '' or len(response) > 140):
            response = '%s %s' % (user, insults[random.randint(0,96)])
        self.post_tweet(response)
    
    def compliment(self, tweet):
        compliments = open('compliments.txt').read().split('\n')
        text = tweet['text']
        user = text[0]
        response = ''

        while (response == '' or len(response) > 140):
            response = '%s %s' % (user, compliments[random.randint(0,45)])
        self.post_tweet(response)

    def define(self, tweet):
        pass
    
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

#feeble attempt to protect against shelli
        if(fileExt == '.torrent'):
            fileExt = fileExt.strip(';')
            subprocess.call('deluge-console add '+url)
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

    def reminder(self, tweet):
        text = tweet['text']
        user = 'dr_choc'
        #user = tweet['sender']
        time = text[1].split(':')
        reminder = text[3:]

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
        self.post_tweet(response)
 

if __name__ == '__main__':

    # Setup API credentials.
    from secretStuff import *
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Setup Helpy to listen to twitter stream.
    helpy = HelpyBot(api)
    helpy.on_status('@Helpy_bot insult @thompson if you would be so kind.')
    helpy.on_status('@Helpy_bot compliment @ronald if you would be so kind.')
    helpy.on_status('@Helpy_bot isup google.com')
    helpy.on_status('@Helpy_bot isup http://www.google.com')
    #helpy.on_status('@Helpy_bot download http://www.google.com lol.txt')
    helpy.on_status('@Helpy_bot reminder in 1:30 to blah blah blah poop')

    #listener = HelpyBot()
    #stream = Stream(auth, listener)
    #stream.filter(follow=(483102366,),)

