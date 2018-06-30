# System utilities
import sys

# %matplotlib inline

sys.path

# Spotify API
import spotipy
import spotipy.util as util
# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("punkt")

# Word embeddings
# https://nlp.stanford.edu/projects/glove/


from importlib import reload

import genius_api
reload(genius_api)
from genius_api import *

import playlist_class
reload(playlist_class)
from playlist_class import *

import song_class
reload(song_class)
from song_class import song

import playlist_class
reload(playlist_class)
from playlist_class import playlist

sys.path.append("./Word_Embeddings_Related")
import utils_adv
reload(utils_adv)
from utils_adv import *

# Get user playlist information from spotify
#username = 'malchemist02'  #TODO: Make user input
username = "1282829978"
scope = 'playlist-read-private playlist-read-collaborative'  # the permissions to give our application
token = util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(auth=token)

###############################
#### Class functionalities ####
###############################

#########################
# Playlist class object #
#########################

### Create dataframe of playlists for the user ###

# playlists = sp.category_playlists('hiphop') # For using the genre playlists from spotify
playlists = sp.user_playlists(username)  # Returns list of playlists & metadata for the provided user

# Now has list with name and id

playlist_name_id = [(key['name'], key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['items']]  # Extract the metadata for each song of the playlist

playlist_info = pd.DataFrame(playlist_name_id, columns=["Name", "Owner", "Number_of_tracks",
                                                        "Tracklist_id"])  # Set the column names for the playlist metadata
playlist_info = playlist_info.set_index('Name')

playlist_name = "Discover Weekly Archive"
test_playlist_id = playlist_info.loc[playlist_name]["Tracklist_id"]
test_playlist_owner = playlist_info.loc[playlist_name]["Owner"]

### END Create dataframe of playlists for the user ###

# [playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp) for ]
# testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)
# testPlaylist = playlist(playlist_name, test_playlist_id, test_playlist_owner, sp, 100)
playlistName = "Long Playlist"
testPlaylist = playlist(playlist_name=playlistName, tracklist_id="5fMCrRnSy4TauAmM36zrIP", username="random guy", sp=sp, n_tracks=100)
