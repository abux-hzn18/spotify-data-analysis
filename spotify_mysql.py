import mysql.connector
from spotipy import SpotifyClientCredentials
import spotipy
import re
import pandas as pd
from credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
    )
)

db_config = {
        'host' : 'localhost',
    'user' :  'root',
    'password' : 'root',
    'database' : 'spotify_db'
}

connection = mysql.connector.connect(**db_config);
cursor = connection.cursor();

track_url = "https://open.spotify.com/track/6habFhsOp2NvshLv26DqMb";

track_id = re.search( r'track/([a-zA-Z0-9]+)',track_url).group(1);

track =  spotify.track(track_id);

track_data = {
    'Track Name' : track['name'],
    'Artist' : track['artists'][0]['name'],
    'Album' : track['album']['name'],
    'Popularity' : track['popularity'],
    'Duration (mins)' : track['duration_ms']/60000
}

df = pd.DataFrame([track_data]);
df.to_csv("Spotify_track_url_data.csv",index = False);


insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""
cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (mins)']
))
connection.commit()

print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")

cursor.close()
connection.close()