

# Count number of times a word shows up in a playlists
# System utilities

# %matplotlib inline

from importlib import reload

# Spotify API
import spotipy
import spotipy.util as util

import genius_api

reload(genius_api)

import playlist

reload(playlist)
from playlist import *

import song_class
reload(song_class)

import playlist
reload(playlist)
from playlist import playlist

# Get user playlist information from spotify
username = 'malchemist02'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)


playlists = sp.user_playlists(username) # Returns list of playlists & metadata for the provided user
# Now has list with name and id
playlist_name_id = [(key['name'],  key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['items']] # Extract the metadata for each song of the playlist
playlist_name_id
playlist_info = pd.DataFrame(playlist_name_id, columns = ["Name", "Owner", "Number_of_tracks", "Tracklist_id"]) # Set the column names for the playlist metadata
playlist_info.columns
playlist_info
playlist_name = "May 2015"
playlist_info = playlist_info.set_index('Name')
testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)

[song.title for song in testPlaylist.listOfSongs]

testPlaylist.getWordCounts(numb_words = 3)

# All count for each word
allLyrics1 = testPlaylist.allLyrics
splitLyrics = allLyrics1.split()
word_freq = {word:splitLyrics.count(word) for word in set(splitLyrics)}
[(word, word_freq[word]) for word in sorted(word_freq, key=word_freq.get, reverse=False)]


 # Search for word and find count
allLyrics1 = testPlaylist.allLyrics
splitLyrics = allLyrics1.split()
splitLyrics.count("think")

# Count occurance of each word in playlist
wc_df = testPlaylist.getWordCounts()
wc_df.sum(axis = 0).sort_values(ascending = False)


# Words per song in playlist
wc_df = testPlaylist.getWordCounts()
wc_df.sum(axis = 1).sort_values(ascending = False)
