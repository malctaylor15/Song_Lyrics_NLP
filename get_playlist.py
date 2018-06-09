# System utilities
import os
from os import environ
import subprocess
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

# Spotify API
import spotipy
import spotipy.util as util
#nltk.download("stopwords")
#nltk.download("wordnet")
#nltk.download("punkt")

# Word embeddings
# https://nlp.stanford.edu/projects/glove/


from importlib import reload
import GeniusAPI_MT
reload(GeniusAPI_MT)
from GeniusAPI_MT import *

import Spotify_Pulls
reload(Spotify_Pulls)
from Spotify_Pulls import *

import song_class
reload(song_class)
from song_class import song

import playlist
reload(playlist)
from playlist import playlist


def get_playlist(username, playlist_name):
    scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
    token = util.prompt_for_user_token(username,scope)
    sp = spotipy.Spotify(auth=token)

    ### Create dataframe of playlists for the user ###

    #playlists = sp.category_playlists('hiphop') # For using the genre playlists from spotify
    playlists = sp.user_playlists(username) # Returns list of playlists & metadata for the provided user
    # Now has list with name and id
    playlist_name_id = [(key['name'],  key['owner']['id'], key['tracks']['total'], key['id']) \
                        for key in playlists['items']] # Extract the metadata for each song of the playlist
    playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"]) # Set the column names for the playlist metadata
    playlist_info = playlist_info.set_index('Name')

    # Error message if playlist name not in username playlist list
    if playlist_name not in playlist_info.index.values:
        print("Playlist named: ", playlist_name, " not found. Playlist found: ")
        print(playlist_info)
        raise ValueError("Playlist not in playlist list")

    # Initialize a playlist
    testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)

    return(testPlaylist)
