
# coding: utf-8

# In[ ]:

import os
from os import environ
import subprocess
import sys
from pprint import pprint as pp
import spotipy
import spotipy.util as util
from wordcloud import WordCloud
# Set environment variables 
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"


# In[ ]:

import gensim
import re 

    
# ## Functions

# In[ ]:

def get_tracklist(tracklist_id, username):
    allTracks = {}
    results = sp.user_playlist(username, tracklist_id, fields="tracks")
    tracks = results['tracks']
    for i, item in enumerate(tracks['items']):
        track = item['track']
        trackName = track['name'] 
        trackArtist = track['artists'][0]['name']
        allTracks[trackName] = trackArtist
    pp(allTracks)
    return allTracks


# In[ ]:

def get_user_playlists_2(username):
    all_playlist_info = [[playlist["name"], playlist['tracks']['total'], playlist['id']] 
                         for playlist in playlists['items'] 
                         if playlist['owner']['id'] == username]
    return(all_playlist_info)


# In[ ]:

def get_user_playlists(username): 
    
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']


# ## Let's get it running 

# In[ ]:

username = '1282829978'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read'
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)
playlists = sp.user_playlists(username)


# In[ ]:
playlists_info = get_user_playlists_2(username)
playlist_index = 2
tracklist = get_tracklist(playlists_info[2][playlist_index], username)

# In[ ]:

# The location of genius API_MT
sys.path.append('/Users/board/Desktop/Kaggle/Song_Lyrics_NLP')
from GeniusAPI_MT import *
#from GeniusAPI_MT import *


# In[ ]:

lyrics_dict = {}
for song_name, artist in tracklist.items():
    lyrics_dict[song_name] = get_song_lyrics(artist_name=artist, song_title=song_name, headers=headers)


# In[ ]:

lyrics_dict.keys()


# In[ ]:

class song: 
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
        self.lyrics = get_song_lyrics(self.artist, self.title, headers = headers)
        self.wc = WordCloud().generate(self.lyrics)
    def showWordCloud(self):
        self.wc.to_image().show()


# In[ ]:

class playlist:
    def __init__(self, playlist_name, list_of_songs):
        self.playlist_name = playlist_name
        self.list_of_songs = songs

        
    


# In[ ]:

inst1 = song('500 Benz', 'Joey Bada$$' )


# In[ ]:

inst1.showWordCloud().show

# In[ ]:
    
