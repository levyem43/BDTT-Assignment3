# Homework 3 for Big Data Tools and Techniques

This homework goes into using the Spotipy API to get json data based on a Spotify Playlist.
The data then gets inserted into a flushed redis.

Finally, does the following processing:
1. Displays the top 10 tracks and artists based on the popularity
2. Shows a bar graph of the artists with the most amount of tracks on the playlist
3. Displays a graph based on the amount of minutes of each track

# Files needed
The 2 files needed for this to work and are hidden by the .gitignore file:
1. config.yaml which has parameters needed to connect to the local instance of Redis.
2. secrets.py which have the CLIENT_ID and CLIENT_SECRET fields

# Usage
To run this homework, run the following command:
python3 .\spotify_api.py

# PLEASE NOTE
When this homework is run there is a warning:
DeprecationWarning: Redis.hmset() is deprecated. Use Redis.hset() instead.

For some reason Redis.hset() cannot take a dictionary while Redis.hmset() can.

## In Computer Science: "If it aint broke, dont fix it"