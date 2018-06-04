
# coding: utf-8


# System utilities
import os
from os import environ
import subprocess
import sys

# Spotify API
import spotipy
import spotipy.util as util

# NLP Libraries
from wordcloud import WordCloud
from textblob import TextBlob
#import gensim.models.word2vec as w2v
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
import nltk

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Random
import re
from pprint import pprint as pp

from importlib import reload
import GeniusAPI_MT
reload(GeniusAPI_MT)
from GeniusAPI_MT import *

from song import *

import pandas as pd

# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"

def get_tracklist(tracklist_id, username):
    """
    This function takes a spotify tracklist id and spotify username
    and returns a dictionary where the track name is the key.
    This function interacts with the Spotify API to find information
    for each song of a track list

    Inputs:
        tracklist_id = Spotify tracklist id (string)
        username = spotify username (string)

    Output:
        allTracks = dictionary with song artist and track name

    """
    print("Running get_tracklist...")
    allTracks = {}
    results = sp.user_playlist(username, tracklist_id, fields="tracks")
    tracks = results['tracks']
    print("There are ", len(tracks["items"]), " in playlist")
    n = 0
    print("There are ", len(tracks['items']), " items in the playlist")
    for i, item in enumerate(tracks['items']):
        track = item['track']
        trackName = track['name']
        trackArtist = track['artists'][0]['name']
        allTracks[trackName] = trackArtist
        n +=1
        if n % 5 ==0: print("Finished ", n, " songs")
    pp(allTracks)
    return allTracks

def get_tracklist_class(tracklist_id, username, sp):
    """
    This function takes a spotify tracklist and spotify username
    and returns a list of the song class.
    This function interacts with the spotify API to find the artist and trackname
    for each song in the playlist and creates a song object for each song.

    Inputs:
        tracklist_id = Spotify tracklist id (string)
        username = spotify username (string)
        sp = spotipy client connection
    Output:
        allTracks = list of song objects in specified playlist (list of song)


    """
    print("Running get_tracklist_class...")
    allTracks = []
    results = sp.user_playlist(username, tracklist_id, fields="tracks")
    tracks = results['tracks']
    print("There are ", len(tracks['items']), " items in the playlist")
    n = 0
    for i, item in enumerate(tracks['items']):
        track = item['track']
        song_temp = song(track['name'], track['artists'][0]['name'], sp = sp, spotify_id = track['id'])
        allTracks.append(song_temp)
        n +=1
        if n % 5 ==0: print("Finished ", n, " songs")
    print("Completed getting tracks from spotify")
    return allTracks

def get_user_playlists_2(username, playlists):
    """
    This function finds playlist name, number of tracks and spotify tracklist id
    for a given user name. The spotify tracklist id is used in the gettracklist
    functions

    Input:
        username = spotify user name number
        playlists = dictionary from spotipy with details for user playlists
    Output:
        all_playlistinfo = pandas dataframe containing playlist name, number of tracks and
        the spotify tracklist id for each playlist

    """
    print("Running get_user_playlists_2...")
    all_playlist_info = [[playlist["name"], playlist['tracks']['total'], playlist['id']]
                         for playlist in playlists['items']]

    playlist_info = pd.DataFrame(all_playlist_info,
        columns = ["Name", "Number_of_Tracks", "Tracklist_id"])

        return(playlist_info)

def get_user_playlists(username):
    print("Running get_user_playlists...")
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = sp.user_playlist(username, playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']

def get_tracklist_lyrics(tracklist):
    """
    This function takes a list of song (class) and returns a string of
    the concatentated lyrics for all songs in playlist (list of songs).

    Input:
        tracklist = list of songs

    Output:
        lyrics = concatenated lyrics
    """
    print("Running get_tracklist_lyrics...")
    lyrics = str()
    for song in tracklist:
        if song.lyrics != ():
            lyrics = lyrics + song.lyrics
    return(lyrics)


"""
# Import Genius API functions
#sys.path.append('/Users/board/Desktop/Kaggle/Song_Lyrics_NLP')
currentDirectory = os.getcwd()
sys.path.append(currentDirectory)

lyrics_dict = {}
for song_name, artist in tracklist.items():
    lyrics_dict[song_name] = get_song_lyrics(artist_name=artist, song_title=song_name, headers=headers)

print(lyrics_dict.keys())
"""

# ## Let's get it running
