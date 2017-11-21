import os
from os import environ
#import subprocess
#import sys
from pprint import pprint as pp
os.environ['SPOTIPY_CLIENT_ID'] = "d3c68e4eb95942fb9a0ceb508d62c127"
os.environ['SPOTIPY_CLIENT_SECRET'] = "bab6935eaa2f478ea4c47a6c8a96eec8"
os.environ['SPOTIPY_REDIRECT_URI'] = "https://example.com/callback"

kittens = {}
def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        #print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            #track['name']))
        #print(track['name'], track['artists'][0]['name'])
        trackName = track['name'] 
        trackArtist = track['artists'][0]['name']
        kittens[trackName] = trackArtist
    pp(kittens)
    return kittens

def get_tracks(username):
    import spotipy
    import spotipy.util as util

    scope = 'user-library-read playlist-read-private user-top-read'
    #username = '1282829978'

    token = util.prompt_for_user_token(username,scope)#client_id='d3c68e4eb95942fb9a0ceb508d62c127',client_secret='bab6935eaa2f478ea4c47a6c8a96eec8',redirect_uri='http://localhost/')
    
    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print()
                print(playlist['name'])
                print('  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                tracksDict = show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print("Can't get token for", username)
    #sp = spotipy.Spotify()
    return tracksDict
    '''playlists = sp.user_playlists('spotify')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    
    results = sp.search(q='weezer', limit=20)
    for i, t in enumerate(results['tracks']['items']):
        print(' ', i, t['name'])'''
        
        
tracksDict = get_tracks('1282829978')