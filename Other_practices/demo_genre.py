
# Imports
import os
from os import environ
import subprocess
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# Spotify API
import spotipy
import spotipy.util as util
%cd /home/malcolm/Documents/Song_Lyrics_NLP


# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"


username = 'malchemist02'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)

song_name = "Up Down"
search_results1 = sp.search(song_name)
search_results1


# Look for artist id
[key for key in search_results1.keys()]
[key for key in search_results1['tracks'].keys()]
temp_results = [key for key in search_results1['tracks']['items']]
len(temp_results)
temp_results[0].keys()
temp_results[0]['id']
[artist['artists'][0]['name'] for artist in temp_results]

[key for key in search_results1['tracks']['items'][0]['artists'][0]]
search_results1['tracks']['items'][0]['id']
# Found it.. Save it
track_id = search_results1['tracks']['items'][0]['id']
song_results = sp.track(track_id)
song_results

len(song_results['artists'])

artist_id = search_results1['tracks']['items'][0]['artists'][0]['id']
artist_results = sp.artist(artist_id)
artist_results

artist_keys = ['genres' ,'name', 'popularity', 'id', 'followers']

[v for k,v in artist_results.items() if k in artist_keys]
artist_results['followers']['total']



def get_details_from_artist(artist_id, sp):
    """
    This function finds the genres, name, popularity and id for an artist
    This can help us aggregate more information about artists

    Input:
        artist_id = spotify artist id
        sp = spotify connection
    Output:
        details (dict) - keys (value type ) are
            genres (list), name (str), popularity(float), id (str),
             followers(int), number_genres (int)
    """

    artist_results = sp.artist(artist_id)
    artist_keys = ['genres' ,'name', 'popularity', 'id']
    details = {k:v for k,v in artist_results.items() if k in artist_keys}
    details["followers"] = artist_results['followers']['total']
    details["number_genres"] = len(artist_results['genres'])
    return(details)

get_details_from_artist(artist_id, sp)

def get_details_from_song(track_id, sp):
    song_results = sp.track(track_id)
    song_keys = ['id', 'name', 'album',
    'popularity', 'explicit', 'track_number']
    song_dets = {k:v for k,v in song_results.items() if k in song_keys}

    aud_feats = sp.audio_features(track_id)
    audio_feats_keys = ['energy', 'liveness', 'tempo',
    'speechiness', 'acousticness', 'instrumentalness',
     'time_signature', 'danceability', 'key', 'duration_ms',
      'loudness', 'valence', 'mode']
    aud_feats_dets = {k:v for k,v in aud_feats.items() if k in audio_feats_keys}

    number_artist = len(song_results['artists'])

    artist_details = {artist['name'] : get_details_from_artist(artist['id'], sp)
        for artist in song_results['artists']}


dict1 = {"a":2, "b":3}
dict2 = {"a1":2, "b1":3}
dict3 = {**dict1, **dict2}

sp_song = sp.track('1NfNdnuFbTgYpRG0z5bHxv')
sp_song.keys()

(sp_song['artists'][0]['id'])
.keys()

aud_feats = sp.audio_features('1NfNdnuFbTgYpRG0z5bHxv')
aud_feats
aud_feats[0].keys()




[key for key in sp_song.keys()]


[key for key in sp_song.keys()]
len(sp_song['artists'])
artist_ids = {}
for artist_numb in range(0,len(sp_song['artists'])):
    artist_id_temp = sp_song['artists'][artist_numb]['id']
    artist_name_temp = sp_song['artists'][artist_numb]['name']
    artist_ids[artist_name_temp] = artist_id_temp

artist_ids

[key for key in sp_song['artists'][0].keys()]
sp_song['artists'][0]['name']
sp_song['artists'][0]['id']

sp.artist("5WUlDfRSoLAfcVSX1WnrxN")
