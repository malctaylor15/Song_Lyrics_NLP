
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

def get_tracklist_class(tracklist_id, username):
    allTracks = []
    results = sp.user_playlist(username, tracklist_id, fields="tracks")
    tracks = results['tracks']
    for i, item in enumerate(tracks['items']):
        track = item['track']
        song_temp = song(track['name'], track['artists'][0]['name'])
        allTracks.append(song_temp)
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

# In[]:
def get_tracklist_lyrics(tracklist):
    lyrics = str()
    for song in tracklist:
        if song.lyrics != ():
            lyrics = lyrics + song.lyrics
    return(lyrics)


# ## Let's get it running 
# In[ ]:

username = '1282829978'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read'
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)
playlists = sp.user_playlists(username)


# In[ ]:
playlists_info = get_user_playlists_2(username)
pp(playlists_info)
# In[ ]:
playlist_index = 2
tracklist = get_tracklist(playlists_info[playlist_index][2], username)

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
    def showWordCloud(self):
        if self.lyrics == ():
            print("No lyrics found")
            return ()
        self.wc = WordCloud().generate(self.lyrics)
        self.wc.to_image().show()


# In[ ]:

class playlist:
    def __init__(self, tracklist_id, username):
        self.username = username
        self.tracklist_id = tracklist_id
        self.tracklist = get_tracklist_class(self.tracklist_id, self.username)
        self.allLyrics = get_tracklist_lyrics(self.tracklist)
    def showWordCloud(self):
        self.wc = WordCloud().generate(self.allLyrics)
        self.wc.to_image().show()
        

        
    


# In[ ]:

inst1 = song('500 Benz', 'Joey Bada$$' )


# In[ ]:

inst1.showWordCloud()

# In[ ]:
    
Playlist1 = playlist(playlists_info[playlist_index][2], username)

# In[ ]:
Playlist1.showWordCloud().show()

# In[]:
demo = Playlist1.tracklist[4]
print(demo.lyrics)
wc = WordCloud().process_text(demo.lyrics)  
print(wc)


# In[]:
print(len(Playlist1.allLyrics))
print(len(demo.lyrics))


# In[]:
