import streamlit as st
import requests
import numpy as np
import pandas as pd

'''
# Cerveja barata - Zé Delivery
### Descubra as opções de cerveja mais baratas oferecidas pelo Zé Delivery, e filtre de acordo com suas preferências
'''

# Function that calls the API to scrape the delivery website, based on the provided address.
@st.cache
def get_df(params):
    st.write('Isso pode demorar de 1 a 2 minutos.')
    st.write(params)
    response = requests.get(url, params=params)
    st.write(response)
    try:
        data = response.json()
        st.write('Resultado:', response.json()['Response'])
        df = pd.DataFrame.from_dict(data['Response'])
        st.write(df)
        return df
    except: 
        st.write('Ocorreu um erro. Por favor, tente novamente.')
        return None

url = 'https://cheapestbeer2-35giwnmc6q-ew.a.run.app/get_beers'

location = st.text_input('Defina o endereço de entrega.')

params = {'address':str(location),
         'wb':str([]),
         'ub':str([]),
         'r':str(['Yes','No']),
         'mm':'9999'}

if st.button('Pequisar opções de cerveja para esse endereço.'):
    st.write('''Estamos rodando um scraper que vai pesquisar e compilar as cervejas disponíveis
     nesse momento no site do Zé Delivery para o endereço selecionado.
     Isso deve demorar entre 1 a 2 minutos.''')
    get_df(params)


wanted_brands = st.text_input('Escolhas as marcas que você quer incluir*.')
unwanted_brands = st.text_input('Escolhas as marcas que você quer excluir.')
returnable = st.radio('Você deseja incluir:', ('Apenas cervejas não retornáveis', 'Apenas cervejas retornáveis', 'Ambos'))
if returnable == 'Apenas cervejas não retornáveis':
    returnable = ['No']
elif returnable == 'Apenas cervejas retornáveis':
    returnable = ['Yes']
else:
    returnable = ['Yes','No']

max_mls = st.number_input('Escolha o volume máximo da lata/garrafa.')

wanted_brands = []
unwanted_brands = []

if st.button('Filtrar'):
    st.write('Filtros aplicados.')
    df = get_df(params)
    st.write(df)
    # Conditions
    c0 = df['Brand'].isin(wanted_brands) if len(wanted_brands)>0 else df['Brand']==df['Brand']
    c1 = np.logical_not(df['Brand'].isin(unwanted_brands))
    c2 = df['Returnable'].isin(returnable)
    c3 = df['Mls']<=max_mls
    combined_cond = c0&c1&c2&c3

    # Apply conditions
    filtered_df = df[combined_cond]
    filtered_df.reset_index(drop=True,inplace=True)
    st.write(filtered_df)    
else:
    pass