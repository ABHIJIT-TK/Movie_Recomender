import pickle
import streamlit as st
import requests

def get_movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    print(data)
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None

def get_recommendations(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = get_movie_poster(movie_id)
        if poster_url:
            recommended_movie_posters.append(poster_url)
            recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Load movie list and similarity matrix
movies = pickle.load(open('./movie_list.pkl', 'rb'))
similarity = pickle.load(open('./similari_move.pkl', 'rb'))

st.header('Movie Recommender')
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Recommend movie'):
    recommended_movie_names, recommended_movie_posters = get_recommendations(selected_movie)
    num_recommendations = len(recommended_movie_names)
    cols = st.columns(num_recommendations)
    for i in range(num_recommendations):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i], use_column_width='auto')
