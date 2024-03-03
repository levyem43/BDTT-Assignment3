# Homework 3 for Big Data Tools and Techniques

This homework goes into using the Spotipy API to get json data based on a Spotify Playlist.
The data then gets inserted into a flushed redis.

Finally, does the following processing:
1. Displays the top 10 tracks and artists based on the popularity
2. Shows a bar graph of the artists with the most amount of tracks on the playlist
3. Displays a graph based on the amount of minutes of each track

## Setup

- pip install spotipy
- Rename config.yaml.template to config.yaml
- Substitute your Redis details


**Files needed**

The 2 files needed for this to work and are hidden by the .gitignore file:
1. config.yaml which has parameters needed to connect to the local instance of Redis
2. secrets.py which have the CLIENT_ID and CLIENT_SECRET fields

There are templates files with place holders for the code. Remove the ".templates" sufix to have just the files and put in your Spotify Developer and Redis details in the appropriate file.

**Create a Spotify Developer Account for the API**
- Go to [https://developer.spotify.com/](https://developer.spotify.com/) to create one.
- Create an App
- Note: set your Redirect URIs to http://localhost and use your app as a Web API.
- Go to your apps settings to locate your Client ID and Client Secret

**GitHub Repo to clone**
```
git clone https://github.com/levyem43/BDTT-Assignment3.git
cd BDTT-Assignment3
```

**Run the Application**

To run this homework, use the following command:
python3 .\spotify_api.py
