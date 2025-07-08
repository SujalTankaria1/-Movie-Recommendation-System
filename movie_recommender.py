import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.porter import PorterStemmer
import pickle

# Load the datasets
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# Merge the datasets
movies = movies.merge(credits, on='title')

# Select relevant columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast']]

# Remove null values
movies.dropna(inplace=True)

# Function to convert JSON-like strings to lists of names
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

# Function to extract top 3 cast members
def convert3(obj):
    L = []
    counter = 0
    
    # Only use ast.literal_eval if obj is a string
    if isinstance(obj, str):
        obj = ast.literal_eval(obj)
    
    for i in obj:
        if isinstance(i, dict) and counter != 3:
            L.append(i['name'])
            counter += 1
        elif isinstance(i, str):  # Already a list of names
            return obj[:3]
        else:
            break
    return L

# Apply conversion functions
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)

# Convert overview to list of words
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces from genres, cast, and keywords
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])

# Create tags by combining all features
movies['tags'] = movies['overview'] + movies['genres'] + movies['cast'] + movies['keywords']

# Create new dataframe with required columns
new_df = movies[['movie_id', 'title', 'tags']].copy()

# Convert tags to string and lowercase
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# Initialize Porter Stemmer
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

# Apply stemming to tags
new_df['tags'] = new_df['tags'].apply(stem)

# Create count vectorizer
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# Calculate cosine similarity
similarity = cosine_similarity(vectors)

# Recommendation function
def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(new_df.iloc[i[0]].title)
    
    return recommended_movies

# Save the processed data and similarity matrix
pickle.dump(new_df, open('movies.pkl', 'wb'))
pickle.dump(new_df.to_dict(), open('movie_dict.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

# Example usage
if __name__ == "__main__":
    # Test the recommendation system
    print("Movie Recommendation System")
    print("=" * 30)
    
    # Example recommendation
    movie_title = "Avatar"
    print(f"\nRecommendations for '{movie_title}':")
    recommendations = recommend(movie_title)
    for i, movie in enumerate(recommendations, 1):
        print(f"{i}. {movie}")
    
    # Another example
    movie_title = "Batman Begins"
    print(f"\nRecommendations for '{movie_title}':")
    recommendations = recommend(movie_title)
    for i, movie in enumerate(recommendations, 1):
        print(f"{i}. {movie}")
