#!/usr/bin/
cd checkpoints
sqlite3 songs.db

 -- Drop table if exists songs;

create table songs (
  spotify_id TEXT PRIMARY KEY,
  title TEXT,
  artist TEXT,
  raw_lyrics TEXT,
  danceability REAL,
  energy REAL,
  key REAL,
  loudness REAL,
  mode REAL,
  speechiness REAL,
  acousticness REAL,
  instrumentalness REAL,
  liveness REAL,
  valence REAL,
  temp REAL,
  duration_ms REAL,
  time_signature REAL
);

