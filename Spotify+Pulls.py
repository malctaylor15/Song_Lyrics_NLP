
# coding: utf-8

# In[1]:

import os
from os import environ
import subprocess
import sys
from pprint import pprint as pp
import spotipy
import spotipy.util as util

# Set environment variables 
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"


# ## Functions

# In[2]:

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


# In[3]:

def get_user_playlists_2(username):
    all_playlist_info = [[playlist["name"], playlist['tracks']['total'], playlist['id']]
                         for playlist in playlists['items'] 
                         if playlist['owner']['id'] == username]
    return(all_playlist_info)


# In[4]:

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

# In[5]:

username = '1282829978'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read'
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)
playlists = sp.user_playlists(username)


# In[6]:

playlist_info = get_user_playlists_2(username)
playlist_index = 2
tracklist = get_tracklist(playlist_info[playlist_index][2], username)


# In[7]:

playlist_info


# In[8]:

# The location of genius API_MT
sys.path.append('/Users/board/Desktop/Kaggle/Song_Lyrics_NLP')
from GeniusAPI_MT import *
#from GeniusAPI_MT import *


# In[9]:

lyrics_dict = {}
for song_name, artist in tracklist.items():
    lyrics_dict[song_name] = get_song_lyrics(artist_name=artist, song_title=song_name, headers=headers)


# In[10]:

lyrics_dict


# In[ ]:




# In[ ]:




# In[11]:




# In[ ]:

# results = sp.user_playlist(username, playlist['id'], fields="tracks")

# Track name 
# results["tracks"]["items"][0]["track"]["name"]

# Artist 
# results["tracks"]["items"][0]["track"]["artists"][0]["name"]


# In[ ]:

def get_tracks(username):
    #from spotipy.oauth2 import SpotifyClientCredentials
    #import sys
    
    '''
    export SPOTIPY_CLIENT_ID='d3c68e4eb95942fb9a0ceb508d62c127'
    export SPOTIPY_CLIENT_SECRET='bab6935eaa2f478ea4c47a6c8a96eec8'
    export SPOTIPY_REDIRECT_URI='http://localhost/' '''

    #client_credentials_manager = SpotifyClientCredentials('d3c68e4eb95942fb9a0ceb508d62c127','bab6935eaa2f478ea4c47a6c8a96eec8')
    #sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    scope = 'user-library-read playlist-read-private user-top-read'
    #username = '1282829978'
    
    

    '''if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()'''
    token = util.prompt_for_user_token(username,scope)
    #client_id='d3c68e4eb95942fb9a0ceb508d62c127',client_secret='bab6935eaa2f478ea4c47a6c8a96eec8',redirect_uri='http://localhost/')
    


# In[ ]:

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            tracksDict = show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
else:
    print("Can't get token for", username)
#sp = spotipy.Spotify()
return tracksDict
'''playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

results = sp.search(q='weezer', limit=20)
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])'''
    
    


# In[ ]:

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            tracksDict = show_tracks(tracks)
            while tracks['next']:
                tracks = sp.next(tracks)
                show_tracks(tracks)
else:
    print("Can't get token for", username)
#sp = spotipy.Spotify()
'''playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

results = sp.search(q='weezer', limit=20)
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])'''
    
    
#tracksDict = get_tracks('174829003346')


# In[ ]:

#from spotipy.oauth2 import SpotifyClientCredentials
#import sys
username = '174829003346'  
'''
export SPOTIPY_CLIENT_ID='d3c68e4eb95942fb9a0ceb508d62c127'
export SPOTIPY_CLIENT_SECRET='bab6935eaa2f478ea4c47a6c8a96eec8'
export SPOTIPY_REDIRECT_URI='http://localhost/' '''

#client_credentials_manager = SpotifyClientCredentials('d3c68e4eb95942fb9a0ceb508d62c127','bab6935eaa2f478ea4c47a6c8a96eec8')
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = 'user-library-read playlist-read-private user-top-read'
#username = '1282829978'



'''if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()'''
token = util.prompt_for_user_token(username,scope)#client_id='d3c68e4eb95942fb9a0ceb508d62c127',client_secret='bab6935eaa2f478ea4c47a6c8a96eec8',redirect_uri='http://localhost/')

