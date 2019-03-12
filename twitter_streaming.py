# STREAMING TO GET TWEETS

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import os


#Variables that contains the user credentials to access Twitter API
access_token = "183381422-XZnxzRvnqFy68PZ3AWhpxiRZBEI1HeHIuHH1fIs9"
access_token_secret = "kyrjqhraiV9RA4SAzKM5W4jQ6V2OMPRpG3aM19rKTmAUG"
consumer_key = "ToMHR0tsQzfpaKIoBXuKm2n1J"
consumer_secret = "rmuka0OxWTvQzYzKEqLEKW835NLE5nxfxFr5dtV4EgPztwYiFt"

#Basic listener that just prints received tweeets to stdout
class StdOutListener(StreamListener):
	def on_data(self, data):
		# print data
		minSize = 2048
		with open('fetched_tweets.txt', 'a') as tf:
			while os.path.getsize('fetched_tweets.txt') < 1000000000:
				tf.write(data)

		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':
	#handles Twitter authentification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	#filter Twitter Streams to capture data by keywords 
	# stream.filter(track = ['python', 'javascript', 'ruby'])
	stream.filter(locations = [-122.75,36.8,-121.75,37.8])
