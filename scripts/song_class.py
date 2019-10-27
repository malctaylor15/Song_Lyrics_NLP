
import os
from textblob import TextBlob
import pickle
import spotipy
from importlib import reload
import scripts.genius_api as genius

from spotipy.oauth2 import SpotifyClientCredentials

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import numpy as np
import pandas as pd


with open("../cfg_files/genius_header.pkl", 'rb') as hnd:
    genius_headers = pickle.load(hnd)

with open("../cfg_files/spotify_credentials.pkl", "rb") as hnd:
    spotify_credentials = pickle.load(hnd)

os.environ["SPOTIPY_CLIENT_ID"] = spotify_credentials["SPOTIPY_CLIENT_ID"]
os.environ["SPOTIPY_CLIENT_SECRET"] = spotify_credentials["SPOTIPY_CLIENT_SECRET"]
os.environ["SPOTIPY_REDIRECT_URI"] = spotify_credentials["SPOTIPY_REDIRECT_URI"]

class song:
    def __init__(self, title: str, artist: str, spotify_id:str, **kwargs) -> object:
        """
        Creates a song object using the title and artist for a song
        This will get the lyrics and create TextBlob object
        :param title: The song's title
        :param artist: The song's artist
        :param kwargs: Optional parameters
        :rtype: object
        """

        self.title = title
        self.artist = artist
        self.title_and_artist = title + "_" + artist
        self.spotify_id = spotify_id

    def execute(self):
        self.get_genius_lyrics()
        self.get_spotify_audio_features()
        self.get_WordCounts()
        self.get_Sentiment()
        self.summarize()

    def get_genius_lyrics(self):
        self.raw_lyrics = genius.get_song_lyrics(self.artist, self.title, headers = genius_headers)
        self.lyrics = genius.text_cleaner(self.raw_lyrics)
        self.blob = TextBlob(self.lyrics)

    def get_spotify_audio_features(self):
        if (self.spotify_id != None):

            client_credentials_manager = SpotifyClientCredentials(client_id=spotify_credentials['SPOTIPY_CLIENT_ID']
                                                                  , client_secret=spotify_credentials['SPOTIPY_CLIENT_SECRET'])

            token = client_credentials_manager.get_access_token()
            sp = spotipy.Spotify(auth=token)

            audio_feats_keep = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness'
                , 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

            try:
                feats = sp.audio_features(self.spotify_id)[0]
                self.audioFeatures = {k:v for k, v in feats.items() if k in audio_feats_keep}
            except:
                print("Was not able to find audio features for spotify id: "+ self.spotify_id)
                self.audioFeatures = {k: -999 for k in audio_feats_keep}

    def get_Sentiment(self, trace = 0):
        """
        This function uses the lyrics of a song to find the polarity
        using the lyrics as a TextBlob object

        If trace is 1 then it will print the polarity

        Output:
            polarity = polarity of the lyrics of the song (float)
        """

        self.polarity = self.blob.sentiment.polarity
        if trace:
            print("Polarity is ", self.polarity)
        return(self.polarity)

    def get_WordCounts(self):
        """
        Counts the number of times a word is in a song
        """
        vectorizer = CountVectorizer()
        feats = vectorizer.fit_transform([self.lyrics]).toarray()[0]
        vocab = vectorizer.get_feature_names()

        word_counts = pd.Series(feats, index = vocab).T.sort_values(ascending = False)
        self.word_counts = word_counts
        return(word_counts)

    def show_WordCloud(self):
        """
        Uses the lyrics to create a WordCloud image and object
        """
        from wordcloud import WordCloud
        if self.lyrics == ():
            print("No lyrics found")
            return ()
        self.wc = WordCloud().generate(self.lyrics)
        self.wc.to_image().show()

    def get_embeddings(self):
        pass

    def summarize(self, print = False):
        all_details = {}
        # Basics
        all_details["title"] = self.title
        all_details["artist"] = self.artist
        all_details["title_and_artist"] = self.title + "_" + self.artist
        all_details["spotify_id"] = self.spotify_id
        # Lyrics
        all_details["raw_lyrics"] = self.raw_lyrics
        all_details["lyrics"] = self.lyrics
        # Other
        all_details["word_counts"] = self.word_counts.to_dict()
        all_details.update(self.audioFeatures)
        all_details["polarity"] = self.polarity

        self.all_details = all_details.copy()
        if print == True:
            print("keys in self.all_details dict are: ", all_details.keys())
