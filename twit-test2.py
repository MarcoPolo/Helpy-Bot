import sys
import tweepy
from tweepy.streaming import StreamListener, Stream
from secretStuff import *

class Listener ( StreamListener ):
    def on_status( self, status ):
        try:
            print status.author.name, status.text, status.place['full_name']
        except:
            pass
        return
    def on_error(self, status_code):
        if status_code != 406:
            print 'An error has occured! Status code = %s' % status_code
        else:
            print 'Error: 406, It is possible that your bounding box is ' \
                  'not SouthWest longitude, SouthWest latitude, NorthEast ' \
                  'longitude, Northeast Latitude'
        return True
    def on_timeout(self):
        return True


class Listener (StreamListener):
    def on_status(self, status):
        print '-' * 20
        print status.user.screen_name, status.text
        return
 

def main():
	"""
	Go to:

	https://dev.twitter.com/apps/new

	Create an app, agree to the terms, Create your access token (you may need
	to reload the page).

	Replace the CONSUMER KEY, CONSUMER SECRET, ACCESS TOKEN and ACCESS TOKEN
	SECRET with the values generated from the 
	https://dev.twitter.com/apps/xxxxxx/show page

	You don't need to give the app write privileges as it is only
	going to follow the stream and print the messages within the bounding
	box.

	"""
	auth1 = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth1.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth1)
        global dc
        dc=api.get_user('helpy_bot')

	listener = Listener()
	stream = Stream(auth1, listener)

	print dir(stream)
	#stream.userstream('dr_choc')
    #this has to be a user id
	stream.filter(follow=(483102366,),)

# filter messages with the text 'apple'
#stream.filter(None,['apple'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'

#api.update_status(sys.argv[1])
#me = api.user_timeline('dr_choc')
#print dir(me[0])
#print [x.text for x in me]


