# Spotify API
import spotipy
import spotipy.util as util

# System utilities
import os
from os import environ
import subprocess
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline



# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"


#username = 'malchemist02'  #TODO: Make user input
username = "1282829978"
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)
tracklist_id = "37i9dQZF1DWWMOmoXKqHTD"

results = sp.user_playlist(username, tracklist_id, fields="tracks")
tracks = results['tracks']
len(tracks)
tracks["items"][0]["track"].keys()

n_tracks = len(tracks["items"])
n_tracks
playlist_uris = []
for track in range(n_tracks):
    playlist_uris.append(tracks["items"][track]["track"]["uri"])

playlist_uris[:3]


for i, item in enumerate(tracks['items']):
    track = item['track']



# song_temp = song(track['name'], track['artists'][0]['name'], sp = sp, spotify_id = track['id'])
