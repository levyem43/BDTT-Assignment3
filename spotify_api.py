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
    
    playlistDataFrame['popularity'] = playlistDataFrame['popularity'].astype(int)
    
    print(playlistDataFrame.nlargest(10,'popularity')[['artist_name','track_name','popularity']])
    
main()