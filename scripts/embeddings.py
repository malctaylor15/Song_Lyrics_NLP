import pandas as pd
import os
from importlib import reload
import utils_adv
import pandas as pd
import os
import pickle
from scipy.spatial.distance import cosine
from flair.data import Sentence

# reload(utils_adv)
# from utils_adv import *


# Read in the embeddings from the top words list
def get_word_embeddings(glove_path, words, output_freq = 50000, cutoff = None):
    """
    Look in embeddings file and get the matching embeddings

    For each line in the file path, split on spaces and see if the word
    is in the words list

    Inputs:
        glove_path (str): path to embeddings
        words (list): list of words to retrieve from embeddings file
        output_freq (int) : number of words to alert after going through embeddings file
        cutoff (int): how many lines in embeddings to look through (debugging)
    Output:
        embed_dict (dict): keys are word name, value is list of the embeddings
    """

    if not os.path.isfile(glove_path): raise ValueError("Glove file not found: path={}".format(glove_path))

    with open(glove_path, 'r+', encoding='utf-8') as fp:
        i = 0
        embed_dict = {}
        for line in fp:
            split_line = line.split()
            if split_line[0] in words:
                embed_dict[split_line[0]] = split_line[0:]
            i +=1
            if i % output_freq == 0:
                print("Looked through ", i, " words")
            if i == cutoff: break
            if len(embed_dict) == len(words): break

    return(embed_dict)

def get_embeddings(playlist):
    # Get dataframe of all 'songs by words' IF the word appears in the top 200 ranked words
    words_songs_freqs: object = playlist.getWordCounts(min_word_rank=200)

    #  FOR TESTING 20180616 ONLY #
    # Create and unique index for word counts
    temp = [song.title+"_"+song.artist for song in playlist.listOfSongs if song.title in words_songs_freqs.index]
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
    print("Completed get_embeddings")
    return norm_song_embeds

def create_cosine_matrix(norm_song_embeds):

    counter = 0
    song_cosine_dict = {}
    for song in norm_song_embeds.index: # The 50 subset if just for testing 20180616
        embed_check = norm_song_embeds.loc[song]
        temp_single_cosine_list = norm_song_embeds.apply(lambda x: 1 - cosine(x, embed_check), axis=1)
        song_cosine_dict[song] = temp_single_cosine_list.sort_values(ascending=False)
        counter += 1
        if counter % 100 == 0:
            print(f"100 done!\n counter is now {counter}")


    pd_cosine_matrix = pd.concat(song_cosine_dict, axis=1)
    pd_cosine_matrix.to_csv('checkpoints/Cosine_matrix.csv')

    print("Saved cosine matrix")
    print("Cosine matrix is size: ", pd_cosine_matrix.shape)
    #TODO: Make the file name a variable based on the playlist title
    return pd_cosine_matrix

def get_flair_bert_embeddings(words):

    # Experimental -- not tested

    from flair.embeddings import BertEmbeddings


    bert_embedding = BertEmbeddings('bert-base-multilingual-cased')

    sentence = Sentence(words)
    bert_embedding.embed(sentence)

    return(sentence)




