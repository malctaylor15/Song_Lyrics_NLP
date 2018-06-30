import pandas as pd
import os
import pickle
from scipy.spatial.distance import cosine

def cosine_dict_func(norm_song_embeds):

    def save_object(obj, filename):
        with open(filename, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

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

    os.chdir(os.getcwd()+"\\Song_Cosine_Similarities")
    #save_object(song_cosine_dict, f"Song_Cosine_{playlistName}.pkl")
    #TODO: Make the file name a variable based on the playlist title
    # Song that are dissimilar to each other
    print([(song, x[-5:]) for song, x in song_cosine_dict.items()])
    print("Finished cosine_dict_func()...")
    return song_cosine_dict
