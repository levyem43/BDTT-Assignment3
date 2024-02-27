import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
from db_config import get_redis_connection
import secrets1
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from pprint import pprint as pp

DISNEY_PLAYLIST_ID = "37i9dQZF1DX8C9xQcOrE6T"

class Spotify:
    def __init__(self,playlistID):
        self.client_creds_manager = SpotifyClientCredentials(
            client_id=secrets1.CLIENT_ID, client_secret=secrets1.CLIENT_SECRET)
        self.spotify = spotipy.Spotify(client_credentials_manager=self.client_creds_manager)
        self.playlistID = playlistID
        self.playlist = self.spotify.playlist_tracks(playlist_id=self.playlistID)
        
    def getPopularityOfTracks(self):
        return [track['track']['popularity'] for track in self.playlist['items']]
    
    def getAveragePopularity(self):
        nonZeroPops = [pop for pop in self.getPopularityOfTracks() if pop!=0]
        averagePop = round(sum(nonZeroPops)/len(nonZeroPops)) if nonZeroPops else 0
        return averagePop
    
    def getPlaylistData(self):
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
    def __init__(self):
        """
        """
        self.redisConnection = get_redis_connection()
        self.flushAllFromRedis()
    
    def insertDataIntoRedis(self,key,value):
        """
        """
        self.redisConnection.hmset(key,value)
        
    def flushAllFromRedis(self):
        """
        """
        self.redisConnection.flushall()

    def getDataFromRedis(self,key):
        """
        """
        return self.redisConnection.hgetall(key)
    
    def keys(self):
        """"""
        return self.redisConnection.keys()
    

def main():
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
    df['popularity'] = df['popularity'].astype(int)
    
    print("First Processing Output")
    print(df.nlargest(10,'popularity')[['artist_name','track_name','popularity']].to_string(index=False))

def processing2(df):
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
    minutes_per_track = df['duration_minutes'].value_counts().sort_index()
    
    # Plot aggregated results
    plt.figure(2)
    minutes_per_track.plot(kind='bar', figsize=(8, 8))
    plt.title('Amount of Minutes of each track in the playlist')
    plt.yticks(range(0,50,5))
    plt.xlabel('Track Time (in Minutes)')
    plt.ylabel('Amount of Tracks')
    


main()