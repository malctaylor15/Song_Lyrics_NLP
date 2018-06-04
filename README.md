# Song Lyrics

In these scripts, we analyze playlists from spotify based on metrics from spotify and the lyrics of the songs. We are able to retrieve the lyrics from the website genius.com .

Spotify is a music service that allows users to listen to music and create playlists to organize their songs. More information about spotify can be found [here](spotify.com) .

Genius.com is a website dedicated to sharing music knowledge and has lyrics for many songs.

### Spotify API

Spotify has a robust API that allows developers to access several metrics about various songs and users. For more information about the API, we can look at the documentation [here](www.spotify/developer/site )

 In order to access the API, we need to create several access tokens and allow access to the API. We can follow the instructions [here]() .

Some of this aggregation is found in the Spotify_Pull.py script.  We are able to comb through the structure of the API and get the playlists for a specific user.


### Genius API

Genius.com also has an API which we can call to retrieve information about a specific song. Unfortunately the API does not give direct access to the lyrics to the song. Instead the API has information about the song title, artist and a link to the genius page. We scrape the lyrics from the genius site using the python package BeautifulSoup4.

The GeniusAPI_MT.py script and lyrics_from_song_api_path function has more details about how to scrape the lyrics.


### Word Embeddings vs Word Frequency

Word embeddings are dense representations of words in some high dimensional space. More information about word embeddings can be found [here](www.stanfordnlp/glove)

For our purposes, the word embeddings can help us reduce the dimensionality of the song representation. For the lyrical analysis and comparison of songs, we can compare each of the words in each song with other words in other songs. We would treat each word as a separate token and one-hot encode it. We can keep track of the frequency or just keep track of whether the word was in the song. In doing this analysis with only the words tokens, there will be a large sparse matrix which is not very informative as there may not be many overlaps. The matrix will have as many columns as there are unique words in songs we are comparing. The rows can be the songs we are comparing at the time. In addition, the tokens only refer to the frequency of the word in the song and do not have any other representation.

Another type of analysis is to use pretrained embeddings. Pre-trained embeddings come in fixed dimensional space (50, 100, 200 etc) where each word token has representation in that space. These embeddings are generated using a large corpus of text and are optimized such that words that are frequently close to each other in the text are "close" to each other in this other dimensional space. It is important to mention that the embeddings are trained on a corpus and to remember the training corpus when thinking about our analysis.

In producing the analysis, we started with the word frequency matrix before getting the word embeddings. We conduct some analysis around the word frequency but focus mainly on the embeddings. The embeddings should give a better representation of what the song is about (according to the training corpus)

### Embeddings and TSNE

Once we have the word embeddings for each song, we can begin doing different types of analysis. One example would be to use the dimensionality reduction technique of TSNE (t-stochastic neighbors embedding). TSNE can help reduce the high dimensional embedding space to 2 dimensions so we can visualize the embedding space. TSNE reduces dimensionality and is supposed to preserve the local structure as well as the global structure of the points. More information about TSNE can be found [here](AV/TSNE)

This visualization can be found in utils_adv.py script. We decided to plot TSNE 4 times using different random seeds to see if there were any consistencies in the images. TSNE optimizes a randomized set of intializations which can affect the outcome. When looking at the diagrams, we can look for points that are consistently close to and far from each other.

This visualization can be difficult to read as more songs are added.

### TSNE and clustering

After we have the TSNE embeddings, we can also use those points to conduct a clustering exercise. We can use the 2 dimensional points to perform unsupervised clustering. We can vary the number of clusters and which points to label. We can see the points closest to the center of the cluster as well as the points furtherest away from the center of the cluster.

** Future improvements **
In the future, we can use different anamoly detection techniques.
I also plan on running the outlier detection on the embeddings and then plotting the clusters on various TSNE embeddings.   
Another avenue for exploration is to change the words used to determine the song embedding. Currently  we use the top n (200) words across all of the songs. We can use the words from songs minus the stop words. This schema will lead to the embeddings being closer to the actual representation of the song according to the embeddings.   


## Code structure

There are two main classes help aggregate the playlists. The song class has information about each individual song -- title, artist, lyrics and other derived metrics. We can create word clouds and get the sentiment of the song using this class functionality.

The other main class is the playlist class where we can begin doing some standard aggregations. The playlist also contains the list of the song class for easy aggregations. We also initialize the playlist using the information from spotify. We can get the most frequent words across all the songs. We can get a word cloud using the lyrics of all the songs.

The main logic of the scripts are located in main.py and word_embeddings_regressions.py, and  word_embeddings_tsne_viz.py .
