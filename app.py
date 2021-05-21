import streamlit as st
import requests
import pandas as pd

'''
# Cheapest Beer Zé - front-end
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')


'''
Choose inputs
'''

url = 'https://cheapestbeer-35giwnmc6q-ew.a.run.app/get_beers'


location = st.text_input('Digite seu endereço.')
wanted_brands = st.text_input('Escolhas as marcas que você quer incluir*.')
unwanted_brands = st.text_input('Escolhas as marcas que você quer excluir.')
returnable = st.radio('Você deseja incluir:', ('Apenas cervejas não retornáveis', 'Apenas cervejas retornáveis', 'Ambos'))
if returnable == 'Apenas cervejas não retornáveis':
    returnable = ['No']
elif returnable == 'Apenas cervejas retornáveis':
    returnable = ['Yes']
else:
    returnable = ['Yes','No']

milimeters = st.text_input('Escolha o volume máximo da lata/garrafa.')


location = 'Rua Mascarenhas de Morais, 132'
wanted_brands = []
unwanted_brands = ['Skol']
returnable = ['No']
milimeters  = '325'

params = {'address':location,
         'wb':str(wanted_brands),
         'ub':str(unwanted_brands),
         'r':str(returnable),
         'mm':milimeters}




if st.button('Pequisar opções mais baratas.'):
    st.write('Isso pode demorar de 1 a 2 minutos.')
    st.write(params)
    response = requests.get(url, params=params)
    st.write(response)
    data = response.json()
    st.write('Resultado:', response.json()['Response'])
    df = pd.DataFrame.from_dict(data['Response'])
    st.write(df)    
else:
    pass