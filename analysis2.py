# System utilities
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

from importlib import reload
import GeniusAPI_MT
reload(GeniusAPI_MT)
from GeniusAPI_MT import *

import Spotify_Pulls
reload(Spotify_Pulls)
from Spotify_Pulls import *

import song
reload(song)
from song import song

import playlist
reload(playlist)
from playlist import playlist



# Get user playlist information from spotify
username = 'malchemist02'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)

playlists = sp.user_playlists(username)
playlist_name_id = [(key['name'],  key['owner']['id'],key['tracks']['total'] , key['id']) \
                    for key in playlists['items']]
playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"])

playlist_info = playlist_info.set_index('Name')
(playlist_info)


playlist1_name = "Hip-Hop R&B Nation"
playlist1 = playlist(playlist_info.loc[playlist1_name].Tracklist_id, playlist_info.loc[playlist1_name].Owner, sp)



playlist2_name = "Hip Hop Top Tracks"
playlist2 = playlist(playlist_info.loc[playlist2_name].Tracklist_id, playlist_info.loc[playlist2_name].Owner, sp)


playlist1_song_names = [song.title for song in playlist1.listOfSongs]
playlist2_song_names = [song.title for song in playlist2.listOfSongs]

len(playlist1_song_names)
len(playlist2_song_names)

# Songs in both playlists
similar_song_titles = [title for title in playlist1_song_names if title in playlist2_song_names]
len(similar_song_titles)


# Unique artists in each playlist
playlist1_artist_names = list(set([song.artist for song in playlist1.listOfSongs]))
playlist2_artist_names = list(set([song.artist for song in playlist2.listOfSongs]))

len(playlist1_artist_names)
len(playlist2_artist_names)

# Artists in both playlist
similiar_artists = [artist for artist in playlist1_artist_names if artist in playlist2_artist_names]
len(similiar_artists)
similiar_artists

# TODO: add remove 0 sentiment flag to getSentiment function
# Should be an optional flag to not include seniment in list if sentiment is 0
sentiments_1 = playlist1.getSentimentList()
sentiments_2 = playlist2.getSentimentList()
np.mean(sentiments_1)
np.mean(sentiments_2)
