### Started 20180301 ###
# Not working as of 20180609
# Combine multiple playlist?
# Put into separate file for functionality MT_05182018

playlists = list(playlist_info.index)
playlist_info[0:1].index.name
testCompiled = pd.DataFrame(columns=['Title', 'Artist', 'min_word_rank', 'Sentiment'])
end = 0
for cat in playlists:
    if end != 3:
        playlist_name = cat
        testPlaylist = playlist(playlist_info.loc[playlist_name].Tracklist_id, playlist_info.loc[playlist_name].Owner,
                                sp)
        playlist_metadata = [(song.title, song.artist, len(song.lyrics.split()), song.getSentiment()) for song in
                             testPlaylist.listOfSongs]
        playlist_metadata_df = pd.DataFrame(playlist_metadata, columns=["Title", "Artist", "min_word_rank", "Sentiment"])
        playlist_metadata_df.sort_values("Sentiment", ascending=False)
        playlist_clean = playlist_metadata_df[playlist_metadata_df.Sentiment != 0]
        testCompiled = testCompiled.append(playlist_clean, ignore_index='true')
        end += 1
    else:
        continue
testCompiled
good_songs = testCompiled
