# System utilities

# %matplotlib inline

# Spotify API
#nltk.download("stopwords")
#nltk.download("wordnet")
#nltk.download("punkt")

# Word embeddings
# https://nlp.stanford.edu/projects/glove/

from importlib import reload

from Word_Embeddings_Related import get_playlist

reload(get_playlist)
from Word_Embeddings_Related.get_playlist import get_playlist

import playlist_class
reload(playlist_class)

import utils_adv
reload(utils_adv)
from utils_adv import *

from scipy.spatial.distance import cosine
from embeddings import get_word_embeddings


# Get user playlist information from spotify
testPlaylist = get_playlist("malchemist02", "Kanye West – The Life Of Pablo")

######## 05172018

type(testPlaylist)
dir(testPlaylist)

# Get word frequency of top 300 words
words_songs_freqs = testPlaylist.getWordCounts(100)

word_freq_count = words_songs_freqs.sum(axis=0)
word_freq_count = word_freq_count.sort_values(ascending=False)

song_freq_count = words_songs_freqs.sum(axis=1)
song_freq_count = song_freq_count.sort_values(ascending=False)

# Drop songs with no words
words_songs_freqs = words_songs_freqs.drop([x[0] for x in song_freq_count.iteritems() if x[1] == 0],axis = 0)
song_freq_count2 = song_freq_count[song_freq_count != 0]
len(song_freq_count2)
song_freq_count.shape
words_songs_freqs.shape
# words_songs_freqs

# song_freq_count.head()
# word_freq_count.head()
top_words = word_freq_count.index.tolist()

os.getcwd()
if "drose" in os.getcwd():
    glove_filepath = r"C:\Users\drose\OneDrive - University of New Haven\Downloads\glove.6B.50d.txt"
else:
    glove_filepath = "/home/owner/Downloads/glove.6B.50d.txt"

os.path.isfile(glove_filepath)
embed_dict = get_word_embeddings(glove_filepath, top_words)

"""
cutoff = None # 400000 # max

# Read in the embeddings from the top words list
with open(glove_filepath, 'r+', encoding='utf-8') as fp:
    i = 0
    embed_dict = {}
    for line in fp:
        split_line = line.split()
        if split_line[0] in top_words:
            embed_dict[split_line[0]] = split_line[0:]
        i +=1
        if i % 4000 ==0 :
            print("Looked through ", i, " words")
        if i == cutoff: break
        if len(embed_dict) == len(top_words): break
"""
# Validate embeddings
len(embed_dict)
set(list(embed_dict)).symmetric_difference(top_words)
#list(embed_dict.keys())

# Turn embeddings into dictionary
embed_pd = pd.DataFrame(embed_dict).T
embed_pd.set_index(embed_pd.iloc[:,0], inplace = True)
embed_pd.drop([0], axis = 1, inplace = True)
embed_pd2 = embed_pd.apply(pd.to_numeric)

embed_pd2.shape
embed_pd2.head(10)

# Find a word using .loc
#embed_pd.loc["much"]


# from scipy.spatial.distance import cosine

# Of the top words in the playlist, which are closest according to wikipedia
len(embed_pd2.index) # number of apply loops n x n computations
cosine_dict = {}
for word in embed_pd2.index:
    embed_check = embed_pd2.loc[word]
    temp_single_cosine_list = embed_pd2.apply(lambda x: 1 - cosine(x, embed_check), axis = 1)
    cosine_dict[word] = temp_single_cosine_list.sort_values(ascending = False)


list(cosine_dict.keys())
check_word = "night"
check_word in embed_pd2.index
cosine_dict[check_word][:10]

## 05192017

embed_pd2.shape
embed_pd2.head()
words_songs_freqs.shape
word_match_freq = words_songs_freqs.drop([col for col in words_songs_freqs.columns \
if col not in list(embed_dict.keys())],axis = 1)
words_songs_freqs.head()
song_embeds = word_match_freq.dot(embed_pd2)
song_embeds.head()
song_embeds

song_freq_count.head()
song_freq_count.shape
song_embeds.shape

# Normalize embededdings -- some songs have more words than others
norm_song_embeds = song_embeds.divide(song_freq_count2, axis = 0)

norm_song_embeds.head()

song_cosine_dict = {}
for song in norm_song_embeds.index:
    embed_check = norm_song_embeds.loc[song]
    temp_single_cosine_list = norm_song_embeds.apply(lambda x: 1 - cosine(x, embed_check), axis = 1)
    song_cosine_dict[song] = temp_single_cosine_list.sort_values(ascending = False)

# Songs that are similar to each other
[(song, x[:5]) for song, x in song_cosine_dict.items()]
# Song that are dissimilar to each other
[(song, x[-5:]) for song, x in song_cosine_dict.items()]


######## Compare embedding regression to using only the words

dir(testPlaylist)


### Get sentiment as response variable ###
playlist_metadata = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in testPlaylist.listOfSongs ]
playlist_metadata_df = pd.DataFrame(playlist_metadata, columns = ["Title", "Artist", "min_word_rank" ,"Sentiment"]) # Creating dataframe from running the song class on each song of the playlist given
playlist_metadata_df.sort_values("Sentiment", ascending = False)
playlist_metadata_df = playlist_metadata_df[playlist_metadata_df.min_word_rank > 0]
playlist_metadata_df.set_index("Title", inplace = True)
playlist_metadata_df.shape
playlist_metadata_df.sort_values("Sentiment", ascending = False).head()



####### Join embedings df1
embeding_model_df1 = playlist_metadata_df.join(norm_song_embeds)
embeding_model_df1.drop(["Artist"], axis = 1, inplace = True)
embeding_model_df1.shape

### Word freq df
freq_model_df1 = playlist_metadata_df.join(words_songs_freqs)
freq_model_df1.drop(["Artist"], axis = 1, inplace = True)
freq_model_df1.shape # Includes sentiment and # of words
freq_model_df1.head()


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X_em = embeding_model_df1.drop(["Sentiment"], axis = 1)
Y_em = embeding_model_df1["Sentiment"]

X_train, X_test, y_train, y_test = train_test_split(X_em, Y_em)

fit1 = LinearRegression().fit(X_train, y_train)
fit1.score(X_test, y_test)
dir(LinearRegression)



X_nw = freq_model_df1.drop(["Sentiment"], axis = 1)
Y_nw = freq_model_df1["Sentiment"]
X_train, X_test, y_train, y_test = train_test_split(X_nw, Y_nw)

fit2 = LinearRegression().fit(X_train, y_train)
fit2.score(X_test, y_test)
dir(LinearRegression)


########### Use a cosine similarity as dep var... compare performance
song_cosine_dict.keys()
dep_var2 = song_cosine_dict["30 Hours"]

dep_var2.head()
norm_song_embeds.head()

# Create embedding dataframe
dep_embedding = pd.concat([dep_var2, norm_song_embeds], axis = 1)
dep_embedding.rename(columns = {0:"song_cosine"}, inplace = True)

# Create words DataFrame
dep_words = pd.concat([dep_var2, words_songs_freqs], axis = 1)
dep_words.rename(columns = {0:"song_cosine"}, inplace = True)


X_sc_em =  dep_embedding.drop(["song_cosine"], axis = 1)
Y_sc_em = dep_embedding["song_cosine"]

X_train, X_test, y_train, y_test = train_test_split(X_sc_em, Y_sc_em)

fit1 = LinearRegression().fit(X_train, y_train)
fit1.score(X_test, y_test)

X_sc_nw =  dep_words.drop(["song_cosine"], axis = 1)
Y_sc_nw = dep_words["song_cosine"]

X_train, X_test, y_train, y_test = train_test_split(X_sc_nw, Y_sc_nw)
fit1 = LinearRegression().fit(X_train, y_train)
fit1.score(X_test, y_test)
