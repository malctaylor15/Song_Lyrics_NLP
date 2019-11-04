import os
import sys
from glob import glob
import pickle
from importlib import reload
import itertools # for combining the pagination results of get_tracklist_class_iteration()

import genius_api

reload(genius_api)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import pandas as pd
from song_class import song
from pprint import pprint as pp

# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://example.com/callback/"


class playlist:
    def __init__(self, playlist_name: object, tracklist_id: object, username: object, sp: object, n_tracks: object) -> object:
        """
        Playlists are defined by a unique spotify playlist id and username

        Creating a playlist class will initialize the list of song (class) and
        concatentate all the lyrics from each song
        """
        # print("Instantiating a playlist...")
        self.tracklist_name = playlist_name
        self.username = username
        self.tracklist_id = tracklist_id
        self.listOfSongs = get_tracklist_class(self.tracklist_name, self.tracklist_id, self.username, sp, n_tracks)

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
        return (self.sentimentList)

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

    def getWordCounts(self, min_word_rank: object = 200) -> object:
        ### Bag of words functionalitys
        """
        Uses the lyrics for each song to find the top min_word_rank in the playlist
        :rtype: object
        :param min_word_rank: The minimum ranking (based on the playlist words) a word must be in order to be included.
        :return: 
        """
        self.songLyricsList = [song.lyrics for song in self.listOfSongs]
        self.songNames = [song.title for song in self.listOfSongs] # ONLY FOR TESTING 20180616
        #self.songNames = [song.title_and_song for song in self.listOfSongs] # will be used after 20180616
        # del songNames[0] delete later if not needed
        # del self.songLyricsList[0]  delete later if not needed
        vect = CountVectorizer(max_features=min_word_rank)
        vectWordFreq = vect.fit_transform(self.songLyricsList).toarray()
        self.vectNames = vect.get_feature_names()
        self.wordFrequency = pd.DataFrame(vectWordFreq, columns=self.vectNames, index=self.songNames)
        return self.wordFrequency

    def getTfidf(self, min_word_rank=200):
        if not hasattr(self, "wordFrequency"):
            self.getWordCounts(min_word_rank)
        transformer = TfidfTransformer(smooth_idf=False)
        tfidf = transformer.fit_transform(self.wordFrequency.values)
        self.tfidf_df = pd.DataFrame(tfidf.toarray(), columns=self.vectNames, index=self.songNames)
        return self.tfidf_df

    def getSongWordCounts(self, min_word_rank=200):
        """
        Get the frequency of each word in each song
        """
        if not hasattr(self, "wordFrequency"):
            self.getWordCounts(min_word_rank)
        self.SongWordFrequency = self.wordFrequency.sum(axis=1).sort_values(ascending=False)
        return (self.SongWordFrequency)

def get_tracklist_class_iteration(results, tracklist_id, username, sp, n_tracks, songs_completed):
    global songs_searched_this_round
    try:
        tracks = results['items']
    except TypeError:
        pass
    iteration_tracks = []
    n = 0

    for i, item in enumerate(tracks):
        track = item['track']
        track_name = track['name']
        track_artists = track['artists'][0]['name']

        TitleArtist = track_name+track_artists

        try:
            if TitleArtist not in prev_completed_songs:
                song_temp = song(track_name, track_artists, sp=sp, spotify_id=track['id'])
                iteration_tracks.append(song_temp)
                songs_searched_this_round = songs_searched_this_round + 1
        except NameError:
            song_temp = song(track_name, track_artists, sp=sp, spotify_id=track['id'])
            iteration_tracks.append(song_temp)
            songs_searched_this_round = songs_searched_this_round + 1
        n += 1
        if n % 10 == 0: print(f"Finished {n} songs")
        if n % n_tracks == 0: break
    songs_completed = songs_completed + n
    print(f"{songs_completed} tracks completed...")
    return iteration_tracks, songs_completed
def get_tracklist_class(tracklist_name, tracklist_id, username, sp, n_tracks):
    """
    This function takes a spotify tracklist and spotify username
    and returns a list of the song class.

    This function interacts with the spotify API to find the artist and trackname
    for each song in the playlist and creates a song object for each song.

    :type tracklist_id: string
    :type sp: spotipy.
    :param tracklist_id: Spotify tracklist id (string)
    :param username: spotify username (string)
    :param sp: spotipy client connection
    :param n_tracks: limit the number of tracks
    :return: list of song objects in specified playlist (list of song)
    """
    global songs_searched_this_round
    songs_searched_this_round = 0

    global prev_completed_songs

    print("Running get_tracklist_class (getting all the tracks for the specified playlist)...")
    all_tracks = []
    inp_name =  input("What is the pkl file name?")
    for pkl in glob(os.getcwd()+"/checkpoints/*.pkl"):
        if inp_name.lower() in pkl.lower():
            print("Using pkl: ", pkl)
            with open(pkl, 'rb') as input2:
                listOfSongs = pickle.load(input2)
            all_tracks = listOfSongs
        else:
            print("Not using pkl: ", pkl)
    try:
        prev_completed_songs = {(song.title + song.artist) for song in listOfSongs}
    except:
        pass

    songs_completed = 0
    initial_results = sp.user_playlist_tracks(username, tracklist_id, fields="next,total,previous,items(track(name, artists, id))", market="US", limit=n_tracks)
    print("There are ", initial_results["total"], " items in the playlist")
    iteration_tracks, songs_completed = get_tracklist_class_iteration(initial_results, tracklist_id, username, sp, n_tracks, songs_completed=0)
    all_tracks.extend(iteration_tracks)
    next_results = initial_results
    next = initial_results['next']

    def save_object(obj, filename):
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


    z = 0 # for testing
    #print(tracklist_name)
    while next != None:
        if songs_searched_this_round > 5:
            print("Saving completed tracks to pickle file \n\n\n")
            print("len(all_tracks: " + str(len(all_tracks)))
            save_object(all_tracks, f"{tracklist_name}.pkl")
            songs_searched_this_round = 0
        print(f"Starting {next} now...\n")

        next_results = sp.next(next_results)
        iteration_tracks, songs_completed = get_tracklist_class_iteration(results=next_results,tracklist_id=tracklist_id, username=username, sp=sp, n_tracks=n_tracks, songs_completed=songs_completed)
        all_tracks.extend(iteration_tracks)
        next = next_results['next']
        print(f"songs_searched_this_round {songs_searched_this_round}")

        z = z+1     # for testing
        if z == 16:  # for testing, set z to the number of iterations you want done
            break   # for testing

    print("Completed getting tracks from spotify")

    # len(listOfSongs)
    #for sung in listOfSongs:
    print(songs_searched_this_round)
    len(all_tracks)
    return all_tracks


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
                                 columns=["Name", "Number_of_Tracks", "Tracklist_id"])

    return (playlist_info)


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
    return (lyrics)
