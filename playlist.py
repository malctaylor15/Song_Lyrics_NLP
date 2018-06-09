from textblob import TextBlob

from importlib import reload
import GeniusAPI_MT
reload(GeniusAPI_MT)
from GeniusAPI_MT import *


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import numpy as np
import pandas as pd
from song_class import song 
import gensim.models.word2vec as w2v


class playlist:
    def __init__(self, tracklist_id, username, sp):
        """
        Playlists are defined by a unique spotify playlist id and username

        Creating a playlist class will initialize the list of song (class) and
        concatentate all the lyrics from each song
        """
        #print("Instantiating a playlist...")
        self.username = username
        self.tracklist_id = tracklist_id
        self.listOfSongs = get_tracklist_class(self.tracklist_id, self.username, sp)
        self.allLyrics = get_tracklist_lyrics(self.listOfSongs)
        self.songNames = [song.title for song in self.listOfSongs]

    def showWordCloud(self):
        from wordcloud import WordCloud
        self.wc = WordCloud().generate(self.allLyrics)
        self.wc.to_image().show()

    def getSentimentList(self):
        """
        This function uses the list of song (class) from the playlist
        to aggregate the polarity for each song

        Output:
            self.sentimentList = list of polarity for each song (list of float)

        """

        self.sentimentList = [song.getSentiment() for song in self.listOfSongs]
        return(self.sentimentList)

    """
    def buildWord2Vec(self, num_features = 50, context_size = 7, min_word_count = 4):
        downsampling = 1e-1

        self.songs2vec = w2v.Word2Vec(
            sg=1,
            seed=1234,
            size=num_features,
            min_count=min_word_count,
            window=context_size,
            sample=downsampling
            )
        self.songs2vec.build_vocab(self.allLyrics)
        self.songs2vec.train(corpus, total_examples = self.songs2vec.corpus_count
                , epochs = self.songs2vec.iter)

    """

    def getWordCounts(self, numb_words = 200):
        ### Bag of words functionalitys
        """
        Uses the lyrics for each song to find the top numb_words in the playlist
        """
        self.songLyricsList = [song.lyrics for song in self.listOfSongs]
        self.songNames = [song.title for song in self.listOfSongs]
        #del songNames[0] delete later if not needed
        #del self.songLyricsList[0]  delete later if not needed
        vect = CountVectorizer(max_features = numb_words)
        vectWordFreq = vect.fit_transform(self.songLyricsList).toarray()
        self.vectNames = vect.get_feature_names()
        self.wordFrequency = pd.DataFrame(vectWordFreq,columns = self.vectNames, index=self.songNames)
        return self.wordFrequency

    def getTfidf(self, numb_words = 200):
        if not hasattr(self, "wordFrequency"):
            self.getWordCounts(numb_words)
        transformer = TfidfTransformer(smooth_idf=False)
        tfidf = transformer.fit_transform(self.wordFrequency.values)
        self.tfidf_df = pd.DataFrame(tfidf.toarray(),columns = self.vectNames, index=self.songNames)
        return self.tfidf_df

    def getSongWordCounts(self, numb_words = 200):
        """
        Get the frequency of each word in each song
        """
        if not hasattr(self, "wordFrequency"):
            self.getWordCounts(numb_words)
        self.SongWordFrequency = self.wordFrequency.sum(axis=1).sort_values(ascending=False)
        return(self.SongWordFrequency)



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
