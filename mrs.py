import numpy as np
import pandas as pd
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Read the csv file using Pandas
songs = pd.read_csv('songdata.csv')
# Resample 5000 random songs from the entire dataset, drops link, resets the index
# songs = songs.sample(n=5000)
songs = songs.head(100)
songs = songs.drop('link', axis=1).reset_index(drop=True)
# Replaces \n escape sequence in the lyrics to ''
songs['text'] = songs['text'].str.replace(r'\n+', '', regex=True)
# Using TfidVectorizer to calculate TF-IDF value. TF-IDF score represents how important a term across the entire document.
tfidf = TfidfVectorizer(analyzer='word', stop_words='english')
# creates a TF-IDF matrix for each term (column) in each document(row)
lyrics_matrix = tfidf.fit_transform(songs['text'])
# Finds cosine similarity, i.e. cosine of the angle between the two non-vectors to determine how similar they are
cosine_similarities = cosine_similarity(lyrics_matrix)
# Dictionary to store the top 50 most similar songs
similarities = {}

for i in range(len(cosine_similarities)):
    # sort each element in cosine_similarities and get the indexes of the songs.
    similar_indices = cosine_similarities[i].argsort()[:-50:-1]
    # After that, we'll store in similarities each name of the 50 most similar songs.
    # Except the first one that is the same song.
    similarities[songs['song'].iloc[i]] = [(cosine_similarities[i][x], songs['song'][x], songs['artist'][x]) for x in similar_indices][1:]

# Save the similarities dictionary using pickle
with open('similarities.pkl', 'wb') as file:
    pickle.dump(similarities, file)

class ContentBasedRecommender:
    def __init__(self, matrix):
        self.matrix_similar = matrix

    def _print_message(self, song, recom_song):
        rec_items = len(recom_song)
       
        print(f'The {rec_items} recommended songs for {song} are:\n')
        print("---------------------------------------------------------------------------------------------------------------------------------------------------------")

        for i in range(rec_items):
            print(f"Number {i+1}:")
            print(f"{recom_song[i][1]} by {recom_song[i][2]} with {round(recom_song[i][0], 3)} similarity score")
            print("---------------------------------------------------------------------------------------------------------------------------------------------------------")
       
    def recommend(self, recommendation):
        # Get song to find recommendations for
        song = recommendation['song']
        # Get number of songs to recommend
        number_songs = recommendation['number_songs']
        # Get the number of songs most similars from matrix similarities
        recom_song = self.matrix_similar[song][:number_songs]
        # print each item
        self._print_message(song=song, recom_song=recom_song)

# Print a message indicating the pickle file has been saved
print("Similarities dictionary has been saved using pickle.")
