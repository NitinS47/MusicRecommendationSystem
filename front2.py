import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('front3.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

CLIENT_ID = "f90080521be244c18248ea1bbbe35cd8"
CLIENT_SECRET = "c8256344315748cbb0fc6eacf9e2d8cf"


client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    similarity_scores = [] 
    for i in distances[1:6]:
        
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        similarity_scores.append(round(distances[i[0]][1], 5)) 

    return recommended_music_names, recommended_music_posters, similarity_scores

st.header('Music Recommendation System')
music = pickle.load(open('df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_music = st.selectbox(
    "Choose a Song",
    music_list
)

if st.button('Similar Songs'):
    recommended_music_names, recommended_music_posters, similarity_scores = recommend(selected_music)
    
    for i in range(5):
        st.text(f"{recommended_music_names[i]} - Similarity Score: {similarity_scores[i]}")
       
        st.image(recommended_music_posters[i], width=150)  
