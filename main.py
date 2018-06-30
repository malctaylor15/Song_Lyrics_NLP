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

################################
###### Embeddings Analysis #####
################################

# Get dataframe of all 'songs by words' IF the word appears in the top 200 ranked words
words_songs_freqs: object = testPlaylist.getWordCounts(min_word_rank=200)

#  FOR TESTING 20180616 ONLY #
# Create and unique index for word counts
temp = [song.title+"_"+song.artist for song in testPlaylist.listOfSongs if song.title in words_songs_freqs.index]
words_songs_freqs.index = temp
### END 20180616 TESTING ###

# Get pd.Series() of word count across all songs in the playlist
word_freq_count = words_songs_freqs.sum(axis=0).sort_values(ascending=False)

# Get pd.Series() of number of words per song
song_freq_count = pd.Series(words_songs_freqs.sum(axis=1), name="song_freq_count").sort_values(ascending=False)

# Drop songs with no words from both
words_songs_freqs2 = words_songs_freqs[words_songs_freqs.sum(axis=1) != 0]
song_freq_count2 = song_freq_count[song_freq_count != 0]

# Check how many were dropped
word_freq_songs_dropped = words_songs_freqs.shape[0] - words_songs_freqs2.shape[0]
song_freq_songs_dropped = song_freq_count.shape[0] - song_freq_count2.shape[0]

song_freq_count2.head()
words_songs_freqs2.head()
top_words = word_freq_count.index.tolist()

os.getcwd()
if "drose" in os.getcwd():
    glove_filepath = r"C:\Users\drose\OneDrive - University of New Haven\Downloads\glove.6B.50d.txt"
else:
    glove_filepath = "/home/owner/Downloads/glove.6B.50d.txt"

os.path.isfile(glove_filepath)

cutoff = None  # 400000 # max

# Words (keys) & their embeddings (values) read in from the glove file
embed_dict = get_word_embeddings(glove_filepath, top_words)
# Validate embeddings
len(embed_dict)
set(list(embed_dict)).symmetric_difference(top_words)
# list(embed_dict.keys())

# Turn embeddings into dictionary
embed_pd = pd.DataFrame(embed_dict)
embed_pd = embed_pd.T
embed_pd.set_index(embed_pd.iloc[:, 0], inplace=True)
embed_pd.drop([0], axis=1, inplace=True)
embed_pd2 = embed_pd.apply(pd.to_numeric)

# Find a word using .loc
# embed_pd.loc["much"]

from scipy.spatial.distance import cosine

# Of the top words in the playlist, which are closest according to wikipedia
len(embed_pd2.index)  # number of apply loops n x n computations
cosine_dict = {}
for word in embed_pd2.index:
    embed_check = embed_pd2.loc[word]
    temp_single_cosine_list = embed_pd2.apply(lambda x: 1 - cosine(x, embed_check), axis=1)
    cosine_dict[word] = temp_single_cosine_list.sort_values(ascending=False)

#
word_match_freq = words_songs_freqs2.drop([col for col in words_songs_freqs2.columns \
                                  if col not in list(embed_dict.keys())], axis=1)

song_embeds = word_match_freq.dot(embed_pd2)

# Normalize embededdings -- some songs have more words than others

try:
    norm_song_embeds = song_embeds.divide(song_freq_count2, axis=0)
except Exception as e:
    print(e)

norm_song_embeds.head()
counter = 0 # testing 20180616
song_cosine_dict = {}
for song in norm_song_embeds.index: # The 50 subset if just for testing 20180616
    embed_check = norm_song_embeds.loc[song]
    temp_single_cosine_list = norm_song_embeds.apply(lambda x: 1 - cosine(x, embed_check), axis=1)
    song_cosine_dict[song] = temp_single_cosine_list.sort_values(ascending=False)
    counter += 1                                        # testing 20180616
    if counter % 100 == 0:                               # testing 20180616
        print(f"100 done!\n counter is now {counter}") # testing 20180616

print("\nFinished running main() script!\n")
# Songs that are similar to each other, where x = DataFrame of song & cosine distance
print([(song, x[:5]) for song, x in song_cosine_dict.items()])

# Output song_cosine_dict to csv
pd.DataFrame(song_cosine_dict).to_csv(os.getcwd()+"\\Song_Cosine_Similarities\\"+"song_cosine_dictOUTPUT.csv")

def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

os.chdir(os.getcwd()+"\\Song_Cosine_Similarities")
save_object(song_cosine_dict, f"Song_Cosine_{playlistName}.pkl")

# Song that are dissimilar to each other
print([(song, x[-5:]) for song, x in song_cosine_dict.items()])