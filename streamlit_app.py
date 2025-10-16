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
  ref = list(db.collection(u'movies').stream());
  ref_dict = list(map(lambda x: x.to_dict(), ref));
  df = pd.DataFrame(ref_dict);

  return df


def loadByName(name):
  movies = load_dataset()
  movies_names = movies[movies['name'].str.contains(name)]
  return movies_names

def loadByDirector(name):
  movies = load_dataset()
  movies_names = movies[movies['director'].str.contains(name)]
  return movies_names


def get_directors():
  df = load_dataset();
  directors = pd.unique(df['director'])
  return directors

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="moviesitesm")

# titulo Netflix App
st.title('Netflix App')

# subheader/text que diga done using st cache
st.text('Done using st.cache!')

# texto encima de la tabla que muestre el numero de films encontrados en cada accion

# sidebar que tenga un checkbox para mostrar todos los nombres
cbox = st.sidebar.checkbox('Show all films')

if cbox:
  dataset = load_dataset()
  st.subheader('All films:')
  st.dataframe(dataset)

# sidebar: input box para busqueda por nombre y boton buscar film que ejecute la accion
name_input = st.sidebar.text_input('Film title:')
name_btn = st.sidebar.button('Search film by name')

if name_btn:
  results = loadByName(name_input);
  st.dataframe(results);

# sidebar: select_box con los directores y boton filtrar director que ejecute la accion
directores = get_directors();

select_box = st.sidebar.selectbox('Select a director name', tuple(directores))
director_btn = st.sidebar.button('Search film by director')

if director_btn:
    results = loadByDirector(name_input);
    st.dataframe(results);

# sidebar: subheader de agregar nuevo film. Parametros de input: nombre, company en un select_box,  director en un select_box, genre en un select_box, boton crear nuevo filme que ejecute la accion


