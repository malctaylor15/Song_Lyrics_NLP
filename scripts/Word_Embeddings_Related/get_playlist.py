# System utilities

# %matplotlib inline

from importlib import reload

# Spotify API
import spotipy
import spotipy.util as util

import genius_api

# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("punkt")
# Word embeddings
# https://nlp.stanford.edu/projects/glove/
reload(genius_api)

import playlist_class

reload(playlist_class)
from playlist_class import *

import song_class
reload(song_class)

import playlist_class
reload(playlist_class)
from playlist_class import playlist


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
    testPlaylist = playlist_class(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)

    return(testPlaylist)
