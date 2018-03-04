

# Spotify API
import spotipy
import spotipy.util as util
import os
import pandas as pd

# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost/"

username = 'malchemist02'  #TODO: Make user input
scope = 'user-library-read playlist-read-private user-top-read' #the permissions to give our application
token = util.prompt_for_user_token(username,scope)
sp = spotipy.Spotify(auth=token)

sp.trace = True
sp.trace_out = True




search1 = sp.search("Candy Cane Lane", type = "track")
search1
len(search1['tracks'])
[track for track in search1['tracks']]
[item for item in search1['tracks']['items']]
search1['tracks']['items'][0].keys()
search1['tracks']['items'][0]

search1['tracks']['items'][0]['popularity']


search_info = [(track['name'], track['artists'][0]['name'],track['duration_ms'], track['popularity'], track['id']) for track in search1['tracks']['items']]

search_info_pd = pd.DataFrame(search_info, columns = ["Title", "Artist", "Duration", "Popularity", "Spotify_id"])


search_info_pd.head()
spotify_id = search_info_pd.Spotify_id[0]


"""
sp_aud_analysis = sp.audio_analysis(spotify_id)
sp_aud_analysis
"""

sp.audio_features(spotify_id)[0]


sp.tracks([spotify_id])
