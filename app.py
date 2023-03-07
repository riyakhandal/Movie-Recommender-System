import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # poster fetch from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
#Adding a sidebar to the app
st.sidebar.title("Welcome to the Movie Recommender System")
selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Show Recommendation'):
    names,posters = recommend(selected_movie_name)

    st.image(posters[0],width = 300, use_column_width=False)
    st.write(names[0])

    st.image(posters[1],width = 300,use_column_width=False)
    st.write(names[1])

    st.image(posters[2],width = 300,use_column_width=False)
    st.write(names[2])

    st.image(posters[3],width = 300,use_column_width=False)
    st.write(names[3])

    st.image(posters[4],width = 300,use_column_width=False)
    st.write(names[4])