import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

@st.cache
def load_dataset(db):
  ref = list(db.collection(u'movies').stream());
  ref_dict = list(map(lambda x: x.to_dict(), ref));
  df = pd.DataFrame(ref_dict);

  return df

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="moviesitesm")

dbNames = db.collection('names')

# titulo Netflix App
st.title('Netflix App')

# subheader/text que diga done using st cache
st.text('Done using st.cache!')

# texto encima de la tabla que muestre el numero de films encontrados en cada accion

# sidebar que tenga un checkbox para mostrar todos los nombres
cbox = st.sidebar.checkbox('Show all films')

if cbox:
  dataset = load_dataset(db)
  st.dataframe(dataset)
# sidebar: input box para busqueda por nombre y boton buscar film que ejecute la accion

# sidebar: select_box con los directores y boton filtrar director que ejecute la accion

# sidebar: subheader de agregar nuevo film. Parametros de input: nombre, company en un select_box,  director en un select_box, genre en un select_box, boton crear nuevo filme que ejecute la accion


