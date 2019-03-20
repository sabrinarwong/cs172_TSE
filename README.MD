# Final Project
Twitter Search Engine

## Running Final Project
This system uses Docker to run ElasticSearch and Flask.

### Pre-Installations

// install docker
// pip install docker-compose

### To Run System
Run the following commands:

```bash
git clone https://github.com/CS172-UCR/finalproject-yikes.git;
cd finalproject-yikes;
docker pull sabrinarwong/finalproject-yikes:1.0.0; 
docker-compose up;
docker-compose down;
```
To load index,
In a separate terminal:
```bash
cd finalproject-yikes;
./json_index.sh
```

In browser:
<http://0.0.0.0:8005>

To quit docker, ctrl+cgit ;


## About
Using Twitter Stream API to retrieve realtime tweets geo-tagged in the San Francisco, CA area.

The `twitter_streaming.py` program streams for tweets and inserts into `fetched_tweets.json`. The index to store the retrieved tweets is created through ElasticSearch. `set_index.py` is a file that initializes the setting of the index. `insert_index.py` reads through the `fetched_tweets.json`, analyzes each json in the file, and inserts it into ElasticSeach.

As an extension to the parts above, I created a web-based interface using Flask, a python web-development framework. This interface allows the user to see all the tweets retrieved from the index in the first page. Upon querying, the resulting page shows tweets relevant to the user's input and a score on the right side. Scoring, sorting, and ranking are all done with ElasticSeach. Scoring is the sum of all fields relevant to query.

More information about this project in the `FinalReport.pdf`

## Contributing

Sabrina Wong 

swong040@ucr.edu

861195047

