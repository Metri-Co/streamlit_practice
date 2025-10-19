import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

@st.cache_data
def load_dataset():
  """
  This function will load the dataset from the database object. Note: passing the
  database object as an argument to this function will raise an error due to
  unhashable object.
  """
  ref = list(db.collection('movies').stream());
  ref_dict = list(map(lambda x: x.to_dict(), ref));
  df = pd.DataFrame(ref_dict);

  return df


def loadByName(name, df):
  movies = df
  movies_names = movies[movies['name'].str.contains(name)]
  return movies_names

def loadByDirector(name, df):
  movies = df
  movies_names = movies[movies['director'].str.contains(name, regex=False)]
  return movies_names

def loadByGenre(name, df):
  movies = df
  movies_names = movies[movies['genre'].str.contains(name, regex=False)]
  return movies_names

def get_df_info():
  df = load_dataset();

  info = {'directors':pd.unique(df['director']),
          'genres':pd.unique(df['genre']),
          'companies':pd.unique(df['company']),}

  return info

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="moviesitesm")

info = get_df_info()
dataset = load_dataset()


# titulo Netflix App
st.title('Netflix App')

# subheader/text que diga done using st cache
st.text('Done using st.cache!')

# texto encima de la tabla que muestre el numero de films encontrados en cada accion

# sidebar que tenga un checkbox para mostrar todos los nombres
cbox = st.sidebar.checkbox('Show all films')

if cbox:
  st.subheader('All films:')
  st.dataframe(dataset)

# sidebar: input box para busqueda por nombre y boton buscar film que ejecute la accion
name_input = st.sidebar.text_input('Film title:')
name_btn = st.sidebar.button('Search film by name')

if name_btn:
  results = loadByName(name_input, dataset);
  st.dataframe(results);

# sidebar: select_box con los directores y boton filtrar director que ejecute la accion
director_select_box = st.sidebar.selectbox('Select a director name: ', tuple(info['directors']))
director_btn = st.sidebar.button('Filter director')

if director_btn:
    results = loadByDirector(director_select_box, dataset);
    st.dataframe(results);


# sidebar: select_box con los generos y filtrar al seleccionar uno
genre_select_box = st.sidebar.selectbox('Select a genre: ', tuple(info['genres']))
genre_btn = st.sidebar.button('Filter genre')

if genre_btn:
    results = loadByGenre(genre_select_box, dataset);
    st.dataframe(results);


# sidebar: subheader de agregar nuevo film. Parametros de input: nombre, company en un select_box,  director en un select_box, genre en un select_box, boton crear nuevo filme que ejecute la accion
st.sidebar.text('New Film')
new_film_name = st.sidebar.text_input('Name:')

new_company = st.sidebar.selectbox('Company: ', tuple(info['companies']))

new_director = st.sidebar.selectbox('Director: ', tuple(info['directors']))

new_genre = st.sidebar.selectbox('Genre: ', tuple(info['genres']))

create_new_film = st.sidebar.button('Create new film')

# upload to db
if new_film_name and new_company and new_director and new_genre and create_new_film:
  
  new_data = {
          'name':new_film_name,
          'company':new_company,
          'director': new_director,
          'genre':new_genre
      }

  db.collection("movies").add(new_data)
  dataset = load_dataset()

  # end
