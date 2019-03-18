import urllib2
from BeautifulSoup import BeautifulSoup
import requests, json, os, re
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
# from random import randint
import apiKeys		#file for apikey

#Variables that contains the user credentials to access Twitter API
access_token = apiKeys.access_token
access_token_secret = apiKeys.access_token_secret
consumer_key = apiKeys.consumer_key
consumer_secret = apiKeys.consumer_secret

filename = 'data/fetched_tweets.json'
filename1 = 'data/tweet.json'

# looks for URL in tweet content
def FindURL(string): 
    # findall() has been used with valid conditions for urls in string 
	url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
	# print url
	return url

# looks for hashtag in tweet content
def FindHashtag(string):
    # findall() has been used with valid conditions for hashtags in string 
    hashtag = re.findall(r'#(?:[a-zA-Z]|[0-9])+', string) 
    return hashtag

def GetUrlTitles(string):
	# urls = FindURL(string);
	# print(string)
	urlTitles = []
	if string:
		for url in string:
			soup = BeautifulSoup(urllib2.urlopen(url['url']))
			urlTitles.append(soup.title.string)
	return urlTitles

#Basic listener that just prints received tweeets to stdout
class StdOutListener(StreamListener):
	def on_data(self, data):
		if os.path.getsize(filename) < 100000: #1,000,000
			with open(filename1, 'w+') as t:
				t.write(data)
				tweet = json.loads(data)
				parseToES(tweet)
			tf.write(data)
			print(os.path.getsize(filename))
			return True
		return False

	def on_error(self, status):
		print(status)

# load json attributes into elasticsearch
def parseToES(tweet):
	try:
		post_url = "http://localhost:9200/twitter/tweets"
		post_autocomplete_url = "http://localhost:9200/autocomplete/tweets"

		if tweet['truncated']:
			# print("extended")
			text = tweet['extended_tweet']['full_text']
			hashtags = tweet['extended_tweet']['entities']['hashtags']
			urls = tweet['extended_tweet']['entities']['urls']
		else:
			# print("not extended")
			text = tweet['text']
			hashtags = tweet['entities']['hashtags']
			urls = tweet['entities']['urls']

		dic = {
			'tweet_id': tweet['id'],
			'screen_name': tweet['user']['screen_name'],
			'location': tweet['place']['full_name'],
			'tweet': text,
			'timestamp': tweet['created_at'],
		}

		dic_autocomplete = {
			'screen_name': tweet['user']['screen_name'],
			'suggested_screen_name': tweet['user']['screen_name'],
			'location': tweet['place']['full_name'],
			'suggested_location': tweet['place']['full_name'],
			'tweet': text,
		}

		if hashtags:
			dic['hashtags'] = [hashtag['text'] for hashtag in hashtags]
			dic_autocomplete['hashtags'] = [hashtag['text'] for hashtag in hashtags]
			dic_autocomplete['suggested_hashtags'] = [hashtag['text'] for hashtag in hashtags]

		if urls:
			dic['urlTitles'] = GetUrlTitles(urls)
			dic_autocomplete['urlTitles'] = GetUrlTitles(urls)

		headers = {
			'Content-Type': "applicatin/json",
			'cache-control': "no-cache"
		}

		dic = json.dumps(dic)
		dic_autocomplete = json.dumps(dic_autocomplete)

		response = requests.request("POST", post_url, data=dic, headers=headers)
		response_autocomplete = requests.request("POST", post_autocomplete_url, data=dic_autocomplete, headers=headers)

		# if(response.status_code==201):
		# 	print("Values Posted in twitter index")
		# if(response_autocomplete.status_code==201):
		# 	print("Values Posted in autocmplete index")

	except:
		import traceback
		traceback.print_exc()
		pass

if __name__ == '__main__':
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	# initialize
	if filename and filename1 :#and es.indices.exists(index = 'twitter'):
		os.remove(filename)		# big json file
		os.remove(filename1)	# indivisual json to index


	#filter Twitter Streams to capture data by location (san francisco) 
	with open(filename, "a+") as tf:
		stream.filter(locations = [-122.75,36.8,-121.75,37.8])

	stream.disconnect()


