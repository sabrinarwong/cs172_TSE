from flask import Flask, render_template
from routes.search import search_blueprint
# import os

app = Flask(__name__)
app.register_blueprint(search_blueprint)

# @app.route("/")
# def home():
# 	os.system("python set_index.py")
# 	os.system("python twitter_streaming.py")
# 	return render_template(index.html)

# import set_index
# import twitter_streaming
if __name__ == "__main__":
	app.run("0.0.0.0",port=8005,debug=False,threaded=True)