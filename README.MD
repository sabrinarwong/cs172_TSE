# TBF

# Final Project
Twitter search engine

## Running PS2
Run the following commands:

```bash
git clone https://github.com/CS172-UCR/finalproject-yikes.git;
cd finalproject-yikes;
docker build -t sabrinarwong/finalproject-yikes:1.0.0 .;
docker push sabrinarwong/finalproject-yikes:1.0.0;
docker-compose up;
python set_index.py && python twitter_streaming.py;
```

## About
Included in this repo is: 


## Issues
1. adding the titles of URL as attribute to JSON, instead it is added into elastic search when indexing

## Assumptions


## Contributing

Sabrina Wong 

swong040@ucr.edu

861195047


<!-- docker build -t sabrinarwong/finalproject-yikes:1.0.0 .; docker push sabrinarwong/finalproject-yikes:1.0.0; docker-compose up;
 -->