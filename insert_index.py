try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

from bs4 import BeautifulSoup
import requests, json, os, re

filename = 'data/fetched_tweets.json'

def GetUrlTitles(urls):
	urlTitles = []
	if urls:
		for url in urls:
			soup = BeautifulSoup(urlopen(url['url']), "html.parser")
			# if soup not in urlTitles:
			urlTitles.append(soup.title.string)
	return urlTitles

# load json attributes into elasticsearch
def parseToES(tweet):
	try:
		post_url = "http://localhost:9200/twitter/tweets"

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

		if hashtags:
			dic['hashtags'] = [hashtag['text'] for hashtag in hashtags]

		if urls:
			dic['urlTitles'] = GetUrlTitles(urls)

		headers = {
			'Content-Type': "applicatin/json",
			'cache-control': "no-cache"
		}

		dic = json.dumps(dic)

		response = requests.request("POST", post_url, data=dic, headers=headers)

		if(response.status_code==201):
			print("Values Posted in twitter index")

	except:
		import traceback
		traceback.print_exc()
		pass

if __name__ == '__main__':
	# initialize
	if os.path.isfile(filename):#and es.indices.exists(index = 'twitter'):
		with open(filename, "r+") as tf:
			for line in tf:
				tweet = json.loads(line)
				parseToES(tweet)
