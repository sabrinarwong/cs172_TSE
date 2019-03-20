# part 1 crawling
# (good)	twitter streaming api to collect geolocated tweets 
# (good)	store in one large file
# 
# (good)	from json check if text contains a URL
# (good)	if a tweet contains a url to an html page, 
# (good) 		get title of that page
# 		add title as addition field of tweet (include it in JSON)

# part 2 retrieval
# (good)	parse json objects and insert into lucene/ES
# (good)	handle fields like username, location, etc.
# (good)	test for retrieval of relevant documents given a query

# part 3 extension
# (good)	web-based interface (flask)
# (good)	- contain a textbox and search button
# (good)	- list of results (first 10) and their scores > decreasing order
# 	- twitter:
# (good)	order by combination of time and relevance
# (god)	describe ranking function
# (good)	use web dev of choice - flask

from flask import Flask, render_template
from routes.search import search_blueprint

# import subprocess
# import os
# print("Creating index from json.")
# print("Index created.")

app = Flask(__name__)
app.register_blueprint(search_blueprint)

if __name__ == "__main__":
	# subprocess.call("json_index.sh", shell=True)

	app.run("0.0.0.0",port=8005,debug=False,threaded=True)