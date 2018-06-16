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

#####################
# Song Class Object #
#####################

"""testSong = song('Free Bird', 'Lynyrd Skynyrd') #instantiate a song class object
testSong.getSentiment() # Defines a song class attribute 'polarity'
testSong.showWordCloud()
testSong.getWordCounts()[testSong.getWordCounts() > 3]
print("Test Song Polarity: %s" % testSong.polarity) # Prints same result as getSentiment() calculates"""

#########################
# Playlist class object #
#########################

### Create dataframe of playlists for the user ###

# playlists = sp.category_playlists('hiphop') # For using the genre playlists from spotify
playlists = sp.user_playlists(username)  # Returns list of playlists & metadata for the provided user
# Now has list with name and id
playlists
playlist_name_id = [(key['name'], key['owner']['id'], key['tracks']['total'], key['id']) \
                    for key in playlists['items']]  # Extract the metadata for each song of the playlist
playlist_name_id
playlist_info = pd.DataFrame(playlist_name_id, columns=["Name", "Owner", "Number_of_tracks",
                                                        "Tracklist_id"])  # Set the column names for the playlist metadata
playlist_info = playlist_info.set_index('Name')
playlist_info.columns
keyword = "Sing"
[x for x in playlist_info.index if keyword in x]
playlist_name = "Discover Weekly Archive"
test_playlist_id = playlist_info.loc[playlist_name]["Tracklist_id"]
test_playlist_owner = playlist_info.loc[playlist_name]["Owner"]

### END Create dataframe of playlists for the user ###
# [playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp) for ]
# testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner, sp)
#testPlaylist = playlist(playlist_name, test_playlist_id, test_playlist_owner, sp, 100)
testPlaylist = playlist("Long Playlist", "5fMCrRnSy4TauAmM36zrIP", "random guy", sp, 100)

### Playlist analysis ###
# Reformat the playlist metadata as a list of items to be turned to a dataframe in the next line
playlist_metadata = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in testPlaylist.listOfSongs]

playlist_metadata_df = pd.DataFrame(playlist_metadata, columns=["Title", "Artist", "min_word_rank",
                                                                "Sentiment"])  # Creating dataframe from running the song class on each song of the playlist given
# Sort on Sentiment column
playlist_metadata_df.sort_values("Sentiment", ascending=False)

# Filter out songs that do not have a Sentiment value
good_songs = playlist_metadata_df[playlist_metadata_df.Sentiment != 0]

# Number of songs before
num_songs_before = len(playlist_metadata)
# Number of songs after
num_songs_after =  len(good_songs)
# Number songs dropped
num_songs_dropped = num_songs_after- num_songs_before
# Percentage drop
pcnt_songs_dropped = (1 - num_songs_before / num_songs_after) * 100

good_songs.min_word_rank.describe()
good_songs.min_word_rank.plot(kind="hist")

good_songs.Sentiment.mean()
good_songs.Sentiment.plot(kind="hist")

###Gather song count by artist###
artist_gb = good_songs.groupby("Artist")
artist_count_all = artist_gb.Title.count()  # Not what I wanted but g
np.sort(artist_count_all)

### Gather the average sentiment for the songs of an artist with mroe than 1 song###
artist_count2 = artist_gb.agg({"Title": "count", "Sentiment": "mean"})[artist_gb.count().Title > 1].sort_values(
    "Sentiment", ascending=False)
artist_count2.sort_values(by="Title", ascending=False)

### Song analysis ###
song_demo = testPlaylist.listOfSongs[1]
song_demo.getWordCounts()
song_demo.title

vect = CountVectorizer()
words = [word for word in song_demo.lyrics.split()]

len([word for word in song_demo.lyrics.split() if word == "tu"])

words[:4]
[song_demo.lyrics]
feats = vect.fit_transform([song_demo.lyrics]).toarray()[0]
song.getWordCounts(song_demo)
pd.Series(feats, index=vect.get_feature_names()).T.sort_values(ascending=False)
feats

###################################################
song_lyrics = [song.lyrics for song in testPlaylist.listOfSongs]
songLyricsNonEmpty = [lyrics for lyrics in song_lyrics if lyrics != ' ']
songLyricsNonEmpty

lyrics1 = ''
for lyrics in songLyricsNonEmpty:
    lyrics1 = lyrics1 + " " + lyrics  # Combine the lyrics of all the songs into one string
lyrics1
len(lyrics1)
len(nltk.word_tokenize(lyrics1))
demoLyrics = list(set(nltk.word_tokenize(lyrics1)))
demoLyrics.sort()
demoLyrics

songLyricsNonEmpty = [lyrics1 + lyrics for lyrics in songLyricsNonEmpty]
songLyricsNonEmpty
' '.join(songLyricsNonEmpty)
testPlaylist.getWordCounts().iloc[0]
testPlaylist.getTfidf()
wordFrequency = testPlaylist.getWordCounts()
wordFrequency
#############################################################

### Get the words showing in all the songs of a playlist ### 20180129
songList = testPlaylist.getTfidf()  # .drop("F**kin' Problems",axis=0)
songList.T[songList.apply(lambda col: col.all((0)), axis=0)]

# wc1 = WordCloud().generate(wc_corpus)
# wc1.to_image().show()

### END PLaylist analysis ###