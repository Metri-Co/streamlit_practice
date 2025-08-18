import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

def load_dataset(db):
  ref = list(db.collection(u'movies').stream());
  ref_dict = list(map(lambda x: x.to_dict(), ref));
  df = pd.DataFrame(ref_dict);

  return df

# df = load_dataset(db)


def loadByName(name):
  names_ref= dbNames.where(u'name', u'==', name)
  currentName = None
  for myname in names_ref.stream():
    currentName = myname
    #end for
  #end
  return currentName

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="moviesitesm")

dbNames = db.collection('names')

st.sidebar.subheader('Buscar nombre');
nameSearch=st.sidebar.text_input('nombre');
btnFiltrar=st.sidebar.button('Buscar');


if btnFiltrar:
  doc = loadByName(nameSearch)
  if doc is None:
    st.sidebar.write(
        'Registro no encontrado'
    )
  else:
    st.sidebar.write(doc.to_dict())
  # end if



st.sidebar.markdown("""----""")
btnEliminar = st.sidebar.button('Eliminar')

if btnEliminar:
  deleteName = loadByName(nameSearch)
  if deleteName is None:
    st.sidebar.write(f"{nameSearch} no existe")
  else:
    dbNames.document(deleteName.id).delete()
    st.sidebar.write(f"{nameSearch} eliminado")
    #end if
  # end if



st.sidebar.markdown("""----""")
newName = st.sidebar.text_input('Nuevo nombre al registro')
btnUpdate = st.sidebar.button('Actualizar')

if btnUpdate:
  updateName = loadByName(nameSearch);
  if updateName is None:
    st.sidebar.write(f"{nameSearch} no existe")
  else:
    myUpdateName = dbNames.document(updateName.id)
    myUpdateName.update(
        {
            'name': newName
        }
    )
    st.sidebar.write(f"{nameSearch} actualizado a {newName}")
  # end if

st.header('Crea un nuevo registro')

index=st.text_input('Index')
name=st.text_input('Name')
sex=st.selectbox('Select sex', ('F', 'M', 'Other'))

submit=st.button('Crear nuevo registro')

# upload to db
if index and name and sex and submit:
  doc_ref=db.collection('names').document(name)
  doc_ref.set(
      {
          'index':index,
          'name':name,
          'sex':sex
      }
  )

  st.sidebar.write('Registro existoso')
  # end

names_ref = list(db.collection(u'names').stream());
names_dict = list(map(lambda x: x.to_dict(), names_ref));
names_dataframe = pd.DataFrame(names_dict);

st.dataframe(names_dataframe);
