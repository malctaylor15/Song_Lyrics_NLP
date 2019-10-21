# System utilities
import sys


# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("punkt")

# Word embeddings
# https://nlp.stanford.edu/projects/glove/


# Spotify API
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime


from importlib import reload
import pickle
import embeddings

import playlist_class
reload(playlist_class)
from playlist_class import *


# Get user playlist information from spotify
#username = 'malchemist02'  #TODO: Make user input
username = "1282829978"
scope = 'playlist-read-private playlist-read-collaborative'  # the permissions to give our application
with open('credentials.pkl', 'rb') as hnd:
    credentials = pickle.load(hnd)
client_credentials_manager = SpotifyClientCredentials(client_id=credentials['SPOTIPY_CLIENT_ID']
                                                      , client_secret=credentials['SPOTIPY_CLIENT_SECRET'])

token = client_credentials_manager.get_access_token()
sp = spotipy.Spotify(auth=token)

#########################
# Playlist class object #
#########################

### Create dataframe of playlists for the user ###

playlists = sp.category_playlists('hiphop') # For using the genre playlists from spotify
# playlists = sp.user_playlists(username)  # Returns list of playlists & metadata for the provided user

# Now has list with name and id

playlist_name_id = [(key['name'], key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['playlists']['items']]  # Extract the metadata for each song of the playlist

playlist_info = pd.DataFrame(playlist_name_id, columns=["Name", "Owner", "Number_of_tracks",
                                                        "Tracklist_id"])  # Set the column names for the playlist metadata
playlist_info = playlist_info.set_index('Name')

# playlist_name = "Discover Weekly Archive"
playlist_name = 'RapCaviar'
test_playlist_id = playlist_info.loc[playlist_name]["Tracklist_id"]
test_playlist_owner = playlist_info.loc[playlist_name]["Owner"]

### END Create dataframe of playlists for the user ###

# [playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp) for ]
# testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)
testPlaylist = playlist(playlist_name, test_playlist_id, test_playlist_owner, sp, 100)

# playlistName = "Long Playlist"
# testPlaylist = playlist(playlist_name=playlistName, tracklist_id="5fMCrRnSy4TauAmM36zrIP", username="random guy", sp=sp, n_tracks=100)
save_name = 'checkpoints/' + "_".join([testPlaylist.tracklist_name, testPlaylist.username, str(datetime.now())]) + '.pkl'
with open(save_name, 'wb') as hnd:
    pickle.dump(testPlaylist, hnd)

# with open(save_name, 'rb') as hnd:
#     testPlaylist = pickle.load(hnd)

# Embeddings #
print("Starting get_embeddings()")
norm_song_embeds = embeddings.get_embeddings(testPlaylist)
##############

# Cosine Dictionary #
print("Starting cosine_dict()")
song_cosine_dicts = embeddings.create_cosine_matrix(norm_song_embeds)
print(list(song_cosine_dicts)[0])
#####################

#TODO: Call TSNE_viz (similar to Cosine Dictionary)