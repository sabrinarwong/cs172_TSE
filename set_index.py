import requests
import json

def check_if_index_present(url):
	response = requests.request("GET", url, data="")
	json_data = json.loads(response.text)
	return json_data

if __name__ == '__main__':
# def main_set_index():
	url = "http://localhost:9200/_template/search_engine_template"
	response = requests.request("GET", url, data="")
	if(len(response.text)>2):
		print("1. Delete template: search_engine_template")
		response_delete = requests.request("DELETE", url)

	payload = {
		"template": "twitter",
		"settings": {
			"number_of_shards": 5
		},
		"mappings":{
			"tweets":{
				"_source":{
					"enabled": True
				},
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
					"text":{
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
		print("3. Deleted an index: twitter")
		response = requests.request('DELETE', url)
	
	response = requests.request("PUT", url)
	if(response.status_code == 200):
		print("4. Created an index: twitter")

	url = "http://localhost:9200/autocomplete"
	json_data = check_if_index_present(url)
	if(not 'error' in json_data):
		print("5. Deleted an index: autocomplete")
		response = requests.request('DELETE', url)

	payload = {
	  	"mappings": {
	   		"titles" : {
	    		"properties" : {
		      		"title" : { "type" : "string" },
		        	"title_suggest" : {
		         		"type" :     "completion",
			          	"analyzer" :  "standard",
			          	"search_analyzer" : "standard",
			          	"preserve_position_increments": False,
			          	"preserve_separators": False
	    			}
	    		}
			}
	  	}
	}
  
	payload = json.dumps(payload)
	response = requests.request("PUT", url, data=payload, headers=headers)
	if(response.status_code == 200):
		print("6. Created an index: autocomplete")
