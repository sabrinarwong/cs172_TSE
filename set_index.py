import requests
import json

def check_if_index_present(url):
	response = requests.request("GET", url, data="")
	json_data = json.loads(response.text)
	return json_data

if __name__ == '__main__':
	url = "http://localhost:9200/_template/search_engine_template"
	response = requests.request("GET", url, data="")
	if(len(response.text)>2):
		print("1. Delete template: search_engine_template")
		response_delete = requests.request("DELETE", url)

	payload = {
		"template": "twitter",
		"settings": {
			"number_of_shards": 5,
        	"index" : {
	            "sort.field" : "timestamp", 
	            "sort.order" : "desc" 
	        }
		},
		"mappings":{
			"tweets":{
				"_all": { "enabled": True, "store": True },
				"_source":{ "enabled": True },
				"properties":{
					"tweet_id":{
						"type": "long"
					},
					"screen_name":{
						"type": "text"
					},
					"location":{
						"type": "text"
					},
					"tweet":{
						"type": "text"
					},
					"timestamp":{
						"type": "text"
					},
					"hashtags":{
						"type": "text"
					},
					"urlTitles":{
						"type": "text"
					},

				}
			}
		}
	}
	payload = json.dumps(payload)
	headers = {
		'Content-Type': "applicatin/json",
		'cache-control': "no-cache"
	}

	response = requests.request("PUT", url, data=payload, headers=headers)
	if(response.status_code == 200):
		print("2. Created a new template: search_engine_template")

	url = "http://localhost:9200/twitter"
	json_data = check_if_index_present(url)
	if(not 'error' in json_data):
		print("1. Deleted an index: twitter")
		response = requests.request('DELETE', url)
	
	response = requests.request("PUT", url)
	if(response.status_code == 200):
		print("2. Created an index: twitter")
