from flask import Blueprint,render_template,request
import requests, json, os

# creating a Blueprint class
search_blueprint = Blueprint('search',__name__,template_folder="templates")
search_term = ""

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
}

@search_blueprint.route("/",methods=['GET','POST'],endpoint='index')
def index():
    if request.method=='GET':
        url = "http://elasticsearch:9200/twitter/tweets/_search"
        query = {
            "query": {
                "match_all": {}
            },
            "size": 50
        }
        response = requests.get(url, data=json.dumps(query),headers=headers)
        response_dict_data = json.loads(str(response.text))
        return render_template('index.html', res=response_dict_data)
        # res ={
        #         'hits': {'total': 0, 'hits': []}
        #      }
        # return render_template("index.html",res=res)
    elif request.method =='POST':
        if request.method == 'POST':
            print("-----------------Calling search Result----------")
            search_term = request.form["input"]
            print("Search Term:", search_term)
            payload = {
                "query": {
                    "multi-match":{
                        "fields": ['*'],
                        "query": search_term,
                    }
                },
                "size": 50,
            }

            payload = json.dumps(payload)
            url = "http://elasticsearch:9200/twitter/tweets/_search"
            response = requests.get(url, data=payload, headers=headers)
            response_dict_data = json.loads(str(response.text))
            return render_template('index.html', res=response_dict_data)



@search_blueprint.route("/autocomplete",methods=['POST'],endpoint='autocomplete')
def autocomplete():
    if request.method == 'POST':
        search_term = request.form["input"]
        print("POST request called")
        print(search_term)
        payload ={
          "autocomplete" : {
                "text" : str(search_term),
                "completion" : {
                    "field" : {
                        "suggested_screen_name", 
                        "suggested_location", 
                        "suggested_hashtags"
                    }
                }
            }
        }
        payload = json.dumps(payload)
        url="http://elasticsearch:9200/autocomplete/_suggest"
        response = requests.request("GET", url, data=payload, headers=headers)
        response_dict_data = json.loads(str(response.text))
        return json.dumps(response_dict_data)