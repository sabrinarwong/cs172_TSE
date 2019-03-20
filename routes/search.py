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
            "size":1000 
        }
        response = requests.get(url, data=json.dumps(query),headers=headers)
        response_dict_data = json.loads(str(response.text))
        return render_template('index.html', res=response_dict_data)

    elif request.method =='POST':
        if request.method == 'POST':
            print("-----------------Calling search Result----------")
            search_term = request.form["input"]
            print("Search Term:", search_term)
            payload = {
                "sort":[
                    {"_score": "desc"}
                ],
                "query": {
                    "multi_match":{
                        "type": "most_fields",
                        "query": search_term,
                        "fields": ["screen_name", "tweet", "location", "hashtags"]
                    }
                },  
                "highlight": {
                    "fields": {
                        "_all": {}
                    }
                },
                "size": 20,
            }

            url = "http://elasticsearch:9200/twitter/tweets/_search"
            response = requests.get(url, data=json.dumps(payload), headers=headers)
            response_dict_data = json.loads(str(response.text))
            print(response_dict_data)
            return render_template('search.html', res=response_dict_data)