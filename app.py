import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(
    page_title="CineMatch AI",
    layout="wide"
)

movies_dict=pickle.load(
open('models/movies.pkl','rb')
)

movies=pd.DataFrame(
movies_dict
)

similarity=pickle.load(
open(
'models/similarity.pkl',
'rb'
)
)

API_KEY="fc4c69e53f9fcbcca1fd2ad40277b675"


def fetch_poster(movie_id):

    url=f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data=requests.get(url)

    data=data.json()

    poster_path=data['poster_path']

    full_path="https://image.tmdb.org/t/p/w500/"+poster_path

    return full_path


def recommend(movie):

    movie_index=movies[
        movies['title']==movie
    ].index[0]

    distances=similarity[
        movie_index
    ]

    movies_list=sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    recommended=[]

    posters=[]

    for i in movies_list:

        movie_id=movies.iloc[
        i[0]
        ].movie_id

        recommended.append(
        movies.iloc[
        i[0]
        ].title
        )

        posters.append(
        fetch_poster(movie_id)
        )

    return recommended,posters

st.title("🎬 CineMatch AI")

st.markdown(
"""
### 🍿 Discover your next favorite movie

Find recommendations powered by Machine Learning and similarity algorithms.
"""
)
selected_movie=st.selectbox(
"Search Movie",
movies['title'].values
)

if st.button(
'Recommend'
):

    with st.spinner(
    'Finding movies...'
    ):    names,posters=recommend(
    selected_movie
    )

    col1,col2,col3,col4,col5=st.columns(5)

    with col1:
        st.image(posters[0])
        st.write(names[0])

    with col2:
        st.image(posters[1])
        st.write(names[1])

    with col3:
        st.image(posters[2])
        st.write(names[2])

    with col4:
        st.image(posters[3])
        st.write(names[3])

    with col5:
        st.image(posters[4])
        st.write(names[4])
st.sidebar.title(
"About CineMatch AI"
)

st.sidebar.info(
"""
Content Based Movie Recommendation System

Built using:

Python  
Scikit-learn  
Streamlit  
TMDB API
"""
)
st.markdown("---")

st.caption(
"Created by Durgashree | CineMatch AI 🎬"
)