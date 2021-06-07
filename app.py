import streamlit as st
import requests
import numpy as np
import pandas as pd

# Page conf
st.set_page_config(
    page_title="Cerveja Barata - Zé Delivery",
    page_icon="🍺",
    layout="wide")

# Hide Streamlit hamburger menu
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.reportview-container .main .block-container{
    padding-top: 0px !important;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Define custom css classes
st.markdown("""
<style>
.very-small-font {
    font-size:11px !important;
}
.small-font {
    font-size:13px !important;
}
.medium-font {
    font-size:15px !important;
}
.subtitle {
    font-size:15px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# Main function that calls the API hosted in GCR to scrape the delivery website, based on the provided address.
@st.cache(suppress_st_warning=True)
def scrape_beers(params):
    response_json = requests.get(api_url, params=params).json()
    response = response_json['Response']
    if response == "Address invalid. Please try again with a valid address.":
        st.write('Endereço inválido. Tente novamente com um endereço válido.')
        return None
    elif response == 'No suppliers open. Try again another time or with another address.':
        st.write('Nenhum distribuidor aberto no momento. Tente novamente mais tarde (horário de funcionamento 10h as 23h BRT.')
        return None
    else:
        df = pd.DataFrame.from_dict(response)
        st.write('Endereço definido. Aplique os filtros para visualizar as cervejas mais baratas.')
        return df

def set_address():
    st.caching.clear_cache()
    st.write('''Estamos rodando um scraper que vai pesquisar e compilar as cervejas disponíveis
     nesse momento no site do Zé Delivery para o endereço selecionado.
     Isso deve demorar entre 1 a 2 minutos.''')
    df = scrape_beers(params)
    
def filter_df():
    df = scrape_beers(params)
    # Conditions
    c1 = np.logical_not(df['Brand'].isin(unwanted_brands))
    c2 = df['Returnable'].isin(returnable)
    c3 = df['Mls']<=max_mls
    combined_cond = c1&c2&c3
    # Apply conditions
    filtered_df = df[combined_cond]
    filtered_df.reset_index(drop=True,inplace=True)
    return df, filtered_df
        
def reduce_df(df):
    df = df[['Product','Price','Price Per Liter','Returnable']]
    return df.head(5)

def to_portuguese(df):
    df.columns = ['Produto','Preço (R$)','Preço p/ Litro','Retornável']
    return df

def style_df(df):
    df = df.style.format({'Preço (R$)': '{:.2f}', 'Preço p/ Litro': '{:.2f}'})
    return df

def treat_df(df):
    df = reduce_df(df)
    df = to_portuguese(df)
    df = style_df(df)
    return df

def display_beers(df1, df2):
    col1.write('Filtros aplicados.')
    st.markdown('<p class="subtitle">Cervejas mais baratas (sem filtro):</p>', unsafe_allow_html=True)
    st.dataframe(df1)
    st.markdown('<p class="subtitle">Cervejas mais baratas (com filtro):</p>', unsafe_allow_html=True)
    st.dataframe(df2)
    st.write('Acesse o Zé Delivery para comprar suas cervejas no link abaixo:')
    st.markdown(ze_url, unsafe_allow_html=True)

#### Page structure ####
st.title('Cerveja barata - Zé Delivery')
st.markdown('Descubra as opções de cerveja mais baratas oferecidas pelo Zé Delivery de acordo com suas preferências.')
st.markdown('')
st.markdown('<p class="subtitle">Passo 1: Defina o endereço de entrega.</p>', unsafe_allow_html=True)
location = st.text_input('Entre com o nome da rua e número. Não inclua o complemento.')

ze_url = 'https://www.ze.delivery/produtos/categoria/cervejas'
api_url = 'https://cheapestbeer2-35giwnmc6q-ew.a.run.app/get_beers'
params = {'address':str(location),
         'wb':str([]),
         'ub':str([]),
         'r':str(['Yes','No']),
         'mm':'9999'}

# Button that sets the address
if st.button('Confirmar endereço.'):
    set_address()    

col1,col2,col3 = st.beta_columns((2,1,1))
col1.markdown('<p class="subtitle">Passo 2: Defina os filtros.</p>', unsafe_allow_html=True)
col2.markdown('<p class="small-font">Quais marcas você quer EXCLUIR da análise?</p>', unsafe_allow_html=True)
col3.write('')
col3.write('')

### Define the filters based on user input
# Filter out brands
unwanted_brands = []
if col2.checkbox('Antarctica'):
    unwanted_brands.append('Antarctica')
if col2.checkbox('Brahma'):
    unwanted_brands.append('Brahma')
if col2.checkbox('Budweiser'):
    unwanted_brands.append('Budweiser')
if col2.checkbox('Serramalte'):
    unwanted_brands.append('Serramalte')
if col2.checkbox('Skol'):
    unwanted_brands.append('Skol')
if col3.checkbox("Beck's"):
    unwanted_brands.append("Beck's")
if col3.checkbox('Bohemia'):
    unwanted_brands.append('Bohemia')
if col3.checkbox('Original'):
    unwanted_brands.append('Original')
if col3.checkbox('Serrana'):
    unwanted_brands.append('Serrana')
if col3.checkbox("Stella Artois"):
    unwanted_brands.append("Stella Artois")

# Filter returnable beers
returnable = col1.radio('Você deseja incluir:', ('Apenas cervejas não retornáveis*', 'Apenas cervejas retornáveis*', 'Ambas'),index=2)
if returnable == 'Apenas cervejas não retornáveis*':
    returnable = ['No']
elif returnable == 'Apenas cervejas retornáveis*':
    returnable = ['Yes']
else:
    returnable = ['Yes','No']
col1.markdown('<p class="very-small-font">* Cervejas retornáveis requerem que você retorne uma garrafa vazia ao entregador.</p>', unsafe_allow_html=True)

# Filter maximum volume
max_mls = col1.number_input('Escolha o volume máximo da lata/garrafa (mls), ou deixe 9999 para incluir tudo.',min_value=0,step=1,value=9999)

# Button to apply filters
if st.button('Buscar cervejas'):
    try:
        unfiltered_df, filtered_df = filter_df()
        treated_unfiltered_df = treat_df(unfiltered_df)
        treated_filtered_df = treat_df(filtered_df)
        display_beers(treated_unfiltered_df, treated_filtered_df)
    except: st.write('Ocorreu um erro. Certifique que o endereço está correto e tente novamente.')
