#####################
# Song Class Object #
#####################
from song_class import song

testSong = song('Free Bird', 'Lynyrd Skynyrd') #instantiate a song class object
testSong.getSentiment() # Defines a song class attribute 'polarity'
testSong.showWordCloud()
testSong.getWordCounts()[testSong.getWordCounts() > 3]
#TODO: Add argument to getWordCount() to limit results to songs with x num of words
print(f"Test Song Polarity: {testSong.polarity}") # Prints same result as getSentiment() calculates