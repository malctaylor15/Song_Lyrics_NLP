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

playlists = sp.user_playlists(username) # Returns list of playlists & metadata for the provided user
playlists

playlist_name_id = [(key['name'],  key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['items']] # Extract the metadata for each song of the playlist
playlist_name_id
playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"]) # Set the column names for the playlist metadata
playlist_info
playlist_name = "May 2015"
playlist_info = playlist_info.set_index('Name')

testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)
testPlaylist
listOfSongs = [song for song in testPlaylist.listOfSongs]
len(listOfSongs)

demo_song = testPlaylist.listOfSongs[0]
demo_song.audioFeatures

[(song.title, song.audioFeatures,song.lyrics) for song in testPlaylist.listOfSongs if song.lyrics != ' '] # Removes songs that Genius API can't find

allSongNames = [song.title for song in listOfSongs]

df2  = pd.DataFrame(columns = ["acousticness", "danceability", "tempo", "valence", "energy", "duration_ms"], index = allSongNames)

for song in testPlaylist.listOfSongs:
    df2.loc[song.title] = {k:v for k,v in song.audioFeatures.items() if k in ["acousticness", "danceability", "tempo", "valence", "energy", "duration_ms"]}
df2.dtypes
df2 = df2.applymap(lambda x: np.float64(x))
df2.mean(axis = 0)
import statsmodels.formula.api as sm
import statsmodels.regression.linear_model as sm2
df = pd.DataFrame({"A": [10,20,30,40,50], "B": [20, 30, 10, 40, 50], "C": [32, 234, 23, 23, 42523]})


result = sm.ols(formula="danceability ~ acousticness + tempo + valence + energy + duration_ms", data=df2).fit()
result.summary()

##
word_counts = testPlaylist.getWordCounts(numb_words= 100)
word_counts.sum(axis = 1)


vect = CountVectorizer(max_features=100)
vectWordFreq = vect.fit_transform(testPlaylist.songLyricsList).toarray()
vectNames = vect.get_feature_names()
vectdf = pd.DataFrame(vectWordFreq,columns = vectNames, index=testPlaylist.songNames)

df3 = df2.join(vectdf)
df3.shape
