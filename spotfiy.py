import re
import matplotlib.pyplot as plt
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
from credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
    )
)

track_url = "https://open.spotify.com/track/2t1pEpxPz91KldW7C0FyZv";

track_id = re.search( r'track/([a-zA-Z0-9]+)',track_url).group(1);

track =  spotify.track(track_id);

# print(track);

track_data = {
    'Track Name' : track['name'],
    'Artist' : track['artists'][0]['name'],
    'Album' : track['album']['name'],
    'Popularity' : track['popularity'],
    'Duration (mins)' : track['duration_ms']/60000
}
# pprint.pprint(track_data);

df = pd.DataFrame([track_data])
print("\nTrack Data as DataFrame:")
print(df)

df.to_csv("Spotify_track_data.csv",index = False);

features = ['Popularity', 'Duration (mins)']
values = [track_data['Popularity'],track_data['Duration (mins)']];

plt.figure(figsize=(8,5))
plt.bar(features, values, color='skyblue', edgecolor='red')
plt.title(f"Track Metadata for '{track_data['Track Name']}'")
plt.ylabel('Value')
plt.show()


