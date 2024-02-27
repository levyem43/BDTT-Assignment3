import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
from db_config import get_redis_connection
import secrets1
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

DISNEY_PLAYLIST_ID = "37i9dQZF1DX8C9xQcOrE6T"

class Spotify:
    """
    A class for interacting with the Spotify API

    Attributes:
    client_creds_manager: Credentials to connect to the Spotify API
    spotify: Instance of the Spotify API
    playlist: Full details of the items of a playlist owned by a Spotify user
    """

    def __init__(self,playlistID):
        """
        Initializes the Spotify object with the provided playlistID

        Args:
        - playlistID: The ID of the spotify playlist
        """
        
        self.client_creds_manager = SpotifyClientCredentials(
            client_id=secrets1.CLIENT_ID, client_secret=secrets1.CLIENT_SECRET)
        self.spotify = spotipy.Spotify(client_credentials_manager=self.client_creds_manager)
        self.playlist = self.spotify.playlist_tracks(playlist_id=playlistID)
        
    def getPopularityOfTracks(self):
        """
        Gets the popularity of all the tracks in the playlist
        
        Returns:
        - A list of popularity rankings for each track in the playlist
        """
        
        return [track['track']['popularity'] for track in self.playlist['items']]
    
    def getAveragePopularity(self):
        """
        Gets the average popularity for each track in the playlist
        
        Returns:
        - The average popularity of all tracks in the playlist
        """
        
        nonZeroPops = [pop for pop in self.getPopularityOfTracks() if pop!=0]
        averagePop = round(sum(nonZeroPops)/len(nonZeroPops)) if nonZeroPops else 0
        return averagePop
    
    def getPlaylistData(self):
        """
        Gets all the data from the playlist in question from the Spotify API
        
        Returns:
        - A list of dictionaries containing information about each track in the playlist
                Each dictionary represents a track and the following keys:
                    - 'artist_name': Name of the artist on the track
                    - 'track_name': The name of the track
                    - 'release_year': The year the track was released
                    - 'duration_minutes': The amount of minutes the track plays
                    - 'duration_seconds': The amount of seconds left to play for the track
                    - 'popularity': The populartiy of the track (The average popularity will be used if the popularity of the track is 0)
                    - 'track_id': The id for the track
        
        I worked with Gabrielle Benson on this method.
        """
        
        playlistData = []
        
        for track in self.playlist['items']:
            popularity = track['track']['popularity']
            
            if popularity == 0:
                popularity = self.getAveragePopularity()
                
            trackData = {
                "artist_name": track['track']['artists'][0]['name'],
                "track_name": track['track']['name'],
                "release_year": track['track']['album']['release_date'].split('-')[0],
                "duration_minutes": track['track']['duration_ms'] // 60000,
                "duration_seconds": (track['track']['duration_ms'] // 1000) % 60,
                "popularity": popularity,
                "track_id": track['track']['id']
            }
            
            playlistData.append(trackData)
        
        return playlistData

class Redis:
    """
    A class to connect to the local instance of Redis

    Attributes:
    redisConnection: Object to connect to redis
    """
    
    def __init__(self):
        """
        Initializes the Redis object and flushes all data from the Redis object to get it to a clean state
        """
        
        self.redisConnection = get_redis_connection()
        self.flushAllFromRedis()
    
    def insertDataIntoRedis(self,key,value):
        """
        Inserts a key value pairing into Redis
        
        Args:
        - key: The key for the redis data being inserted
        - value: The value for the redis data being inserted
        """
        
        self.redisConnection.hmset(key,value)
        
    def flushAllFromRedis(self):
        """
        Flushes all data from Redis
        """
        
        self.redisConnection.flushall()

    def getDataFromRedis(self,key):
        """
        Gets the data from Redis at a specific key
        
        Args:
        key: The key to get the data from Redis
        
        Returns:
        - The value of the key from Redis
        """
        
        return self.redisConnection.hgetall(key)
    
    def keys(self):
        """
        Gets the keys from Redis
        
        Returns:
        - A list of all keys from Redis
        """
        
        return self.redisConnection.keys()
    

def main():
    """
    The main function of this python application.
    """
    
    spotify = Spotify(DISNEY_PLAYLIST_ID)
    playlistData = spotify.getPlaylistData()

    localRedis = Redis()

    for song in range(len(playlistData)):
        key = f"songs:{song}"
        localRedis.insertDataIntoRedis(key,playlistData[song])

    keys = localRedis.keys()
    
    redisData = []
    for key in keys:
        redisInstance = localRedis.getDataFromRedis(key)
        redisData.append(redisInstance)
    
    playlistDataFrame = pd.DataFrame().from_dict(redisData)
    
    processing1(playlistDataFrame)
    
    processing2(playlistDataFrame)
    
    processing3(playlistDataFrame)
    
    # Display the plot
    plt.show()
    
def processing1(df):
    """
    A helper function displaying the top 10 tracks with their artist and popularity rating based on their popularity
    """
    
    df['popularity'] = df['popularity'].astype(int)
    
    print("First Processing Output")
    print(df.nlargest(10,'popularity')[['artist_name','track_name','popularity']].to_string(index=False))

def processing2(df):
    """
    A helper function displaying a pyplot of the number of songs each artist wrote in the playlist for the top 10 artists.
    """
    artist_counts = df['artist_name'].value_counts().nlargest(n=10)
    
    # Plot aggregated results
    plt.figure(1)
    artist_counts.plot(kind='bar', figsize=(8, 10))
    plt.xticks(rotation=30)
    plt.yticks(range(0,5,1))
    plt.title('Number of Songs Each Artist wrote in the playlist')
    plt.xlabel('Artist Names')
    plt.ylabel('Number of Songs')
    
    
def processing3(df):
    """
    A helper function displaying a pyplot of the amount of minutes of each track in the playlist
    """
    minutes_per_track = df['duration_minutes'].value_counts().sort_index()
    
    # Plot aggregated results
    plt.figure(2)
    minutes_per_track.plot(kind='bar', figsize=(8, 8))
    plt.title('Amount of Minutes of each track in the playlist')
    plt.yticks(range(0,50,5))
    plt.xlabel('Track Time (in Minutes)')
    plt.ylabel('Amount of Tracks')
    

main()