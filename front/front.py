import streamlit as st

import numpy as np
import pandas as pd
from datetime import datetime
import requests
from params import ciudades
st.set_page_config(page_title='EnergyAC', page_icon=':bulb:', layout='wide')

# HEADER
with st.container():
    st.subheader('Hi, we are EnergyAC :bulb:')
    st.title('Three datascientist from Argentina')
    st.write('This application allows you to predict the power consumption of an air conditioner in Argentina.')

    
menu = ['Upload your photo', 'Upload your data manually']
choice = st.sidebar.selectbox("Menu", menu)



#############################################
provincias = ['Buenos Aires', 'CABA', ' Catamarca', ' Chaco', 'Chubut', 'Cordoba', 'Corrientes', 'Entre Rios', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquen', 'Rio Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucuman']


localidades = {
    'Buenos Aires': localidades_buenos_aires,
    'Córdoba': ['Rio Cuarto', 'Cordoba']
}

ciudad = st.selectbox('Ciudad', options=provincias)

if ciudad:
    localidad = st.selectbox('Localidad', options=localidades[ciudad])

#############################################

    
if choice == "Upload your photo":
    #METODO 1
    with st.form(key='form1'):
        ciudad = st.selectbox('Choice your city', options=provincia)
        if ciudad:
            bsas_locs['Buenos Aires']
            
        #localidad = st.selectbox('Choice your neighborhood')
        if ciu
        
        submit_button = st.form_submit_button(label="Let's calculate!")
        
    if submit_button:
        params = dict(
                    ciudad=ciudad,
                    localidad=localidad)
        
        #energyac_api_url = 'COLOCAR URL AQUI'
        #response = requests.get(wagon_cab_api_url, params=params)
        
        #prediction = response.json()
        
        #form2= st.form(key='form2')
        
        

      
else:
    st.subheader('Write the AC data here')
        

