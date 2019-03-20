import apiKeys		#file for apikey
import requests, json, os, re
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

#Variables that contains the user credentials to access Twitter API
access_token = apiKeys.access_token
access_token_secret = apiKeys.access_token_secret
consumer_key = apiKeys.consumer_key
consumer_secret = apiKeys.consumer_secret

filename = 'data/fetched_tweets.json'

#Basic listener that just prints received tweeets to stdout
class StdOutListener(StreamListener):
	def on_data(self, data):
		if os.path.getsize(filename) < 1000000: #1,000,000,000 = 1GB
			tf.write(data)
			print(os.path.getsize(filename))
			return True
		return False

	def on_error(self, status):
		print(status)

if __name__ == '__main__':
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	
	# initialize
	if os.path.isfile(filename):
		os.remove(filename)		# big json file
		print("fetched_tweets.txt removed")

	#filter Twitter Streams to capture data by location (san francisco) 
	with open(filename, "a+") as tf:
		stream.filter(locations = [-122.75,36.8,-121.75,37.8])

	stream.disconnect()