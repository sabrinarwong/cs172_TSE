# part 1 crawling
# 	twitter streaming api to collect geolocated tweets
# 	store in one large file
# 
# 	from json check if text contains a URL
# 	if a tweet contains a url to an html page, 
# 		get title of that page
# 		add title as addition field of tweet (include it in JSON)

# part 2 retrieval
# 	parse json objects and insert into lucene/ES
# 	handle fields like username, location, etc.
# 	test for retrieval of relevant documents given a query

# part 3 extension
# 	web-based interface
# 	- contain a textbox and search button
# 	- list of results (first 10) and their scores > decreasing order
# 	- twitter:
#		order by combination of time and relevance
#		describe ranking function
# 	use web dev of choice

#Import the necessary methods from tweepy library
from BeautifulSoup import BeautifulSoup
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
from elasticsearch import Elasticsearch

import apiKeys		#file for apikey
import os, re
import json, requests, urllib2

from datetime import datetime
from flask import Flask, jsonify, request

 

#Variables that contains the user credentials to access Twitter API
access_token = apiKeys.access_token
access_token_secret = apiKeys.access_token_secret
consumer_key = apiKeys.consumer_key
consumer_secret = apiKeys.consumer_secret

filename = 'fetched_tweets.json'
filename1 = 'tweet.json'

res = requests.get('http://localhost:9200')
# print(res.content)
es = Elasticsearch('http://localhost:9200')
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	# results = es.get(index='twitter', doc_type='tweet',id='')
	return '<h1>Welcome!</h1>'

# fix
@app.route('/search', methods=['POST'])
def search():
	keyword = request.form['keyword']

	body = {
		"query": {
			"multi_match": {
				"query": keyword,
				"fields": ["screen_name", "text", "timestamp"]
			}
		}
	}
	res = es.search(index='twitter', doc_type='tweet', body=body)
	return jsonify(res['hits']['hits'])


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
	urls = FindURL(string);
	urlTitles = []
	if urls:
		for url in urls:
			soup = BeautifulSoup(urllib2.urlopen(url))
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
		print status

# load json into elasticsearch
def parseToES(string):

	# json.load(string, tweet)
	try:
		dic = {
			'tweet_id': string['id'],
			'screen_name': string['user']['screen_name'],
			'text': string['text'],
			'timestamp': string['created_at'],
			'location': string['place']['full_name']

		}
		if FindHashtag(string['text']):
			dic['hashtags'] = FindHashtag(string['text'])
		if FindURL(string['text']):
			dic['urlTitles'] = GetUrlTitles(string['text'])
		es.index(index = "twitter", doc_type = 'tweet', body = dic )
		print(json.dumps(dic, ensure_ascii = False))
	except:
		import traceback
		traceback.print_exc()
		pass

# def GetQuery(string):


if __name__ == '__main__':
	#handles Twitter authentification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)

	if filename and filename1 and es.indices.exists(index = 'twitter'):
		os.remove(filename)		# big json file
		print("File removed")
		os.remove(filename1)	# indivisual json to index
		print("File1 removed")
		es.indices.delete(index='twitter', ignore=[400, 404])
		print("Index deleted")

	#filter Twitter Streams to capture data by location (san francisco) 
	with open(filename, "a+") as tf:
		stream.filter(locations = [-122.75,36.8,-121.75,37.8])

	stream.disconnect()

	# parseToES()

app.run(port=5000, debug=True)
