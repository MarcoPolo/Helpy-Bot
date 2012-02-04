import sys
import tweepy
from tweepy.streaming import StreamListener, Stream

class HelpyBot(StreamListener):
	def __init__(self):
		self.commands = ['insult', 'compliment']
		super(HelpyBot, self).__init__()

	def on_error(self, status_code):
		print '[Helpy] Error - status code = %s' % status_code
		return True

	def on_timeout(self):
		return True

	# Parses the given status, and routes it to a command.
	def on_status(self, status):
		tweet = self.parse_status(status)#status.text)

		if (tweet['target'] != '@helpy_bot'):
			print '[Helpy] Tweet not meant for Helpy Bot.'
			return

		if (tweet['command'] in self.commands):
			getattr(self, tweet['command'])(tweet)
		else:
			print '[Helpy] Error - unknown command %s' % tweet['command']

	# Tokenizes the text status.
	def parse_status(self, text):
		tokens = text.lower().split()
		parsed = {}
		parsed['target'] = tokens[0]
		parsed['command'] = tokens[1]
		parsed['text'] = tokens[2:]
		parsed['raw_text'] = ' '.join(tokens[2:])
		return parsed

	# Post text as a tweet to Helpy's account. 
	def post_tweet(self, text):
		print text
			
	def insult(self, tweet):
		print "BUTT"
	
	def compliment(self, tweet):
		print "HOWDY"

	def 

if __name__ == '__main__':

	# Setup API credentials.
	from secretStuff import *
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	# Setup Helpy to listen to twitter stream.
	helpy = HelpyBot()
	helpy.on_status('@Helpy_bot insult @thompson if you would be so kind.')
	helpy.on_status('insult @thompson if you would be so kind.')

	#listener = HelpyBot()
	#stream = Stream(auth, listener)
	#stream.filter(follow=(483102366,),)

