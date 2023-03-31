import streamlit as st
from streamlit_option_menu import option_menu
import requests
from PIL import Image
from energy_ac.gcloud import detect_text
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns



# SET PAGE
st.set_page_config(
    page_title='EnergyAC',
    page_icon=':bulb:',
    layout='wide')

################ESTILOS
with open('style.css') as style_css:
    st.markdown(f"<style>{style_css.read()}</style>", unsafe_allow_html=True)


# PARAMS

provincias = ['', 'Buenos Aires', 'CABA', 'Catamarca', 'Chaco', 'Chubut', 'Cordoba', 'Corrientes', 'Entre Rios', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquen', 'Rio Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucuman']

buenosaires_locs = ['Azul Aero', 'Bahia Blanca Aero', 'Benito Juarez Aero', 'Bolivar Aero', 'Campo de Mayo Aero', 'Coronel Pringles Aero', 'Coronel Suarez Aero', 'Dolores Aero', 'El Palomar Aero', 'Ezeiza Aero', 'Junin Aero', 'La Plata Aero', 'Las Flores Aero', 'Mar del Plata Aero', 'Mariano Moreno Aero', 'Merlo Aero', 'Moron Aero', 'Nueve de Julio', 'Olavarria Aero', ' Pehuajo Aero', 'Pigue Aero', 'Punta Indio B.A.', 'San Fernando', 'Santa Tereista Aero', 'Tandil Aero', 'Trenque Lauquen', 'Tres Arroyos', 'Villa Gesell Aero']

caba_locs = ['Aeroparque Aero' ,'Buenos Aires']

catamarca_locs = ['Catamarca Aero', 'Tinogasta']

chaco_locs = ['Pcia. Roque Saenz peﾑa aero', 'Resistencia Aero']

chubut_locs = ['Comodoro Rivadavia Aero', 'Esquel Aero', 'Paso de Indios', 'Puerto Madryn Aero', 'Trelew Aero']

cordoba_locs = ['Cordoba Aero', 'Cordoba Observatorio', 'Esc.Aviacion Militar Aero', 'Laboulaye Aero', 'Marcos Juarez Aero', 'Pilar Obs.', 'Rio Cuarto Aero', 'Villa Dolores Aero', 'Villa Maria Del Rio Seco']

corrientes_locs = ['Corrientes Aero', 'Ituzaingo', 'Mercedes Aero (ctes)', 'Monte Caseros Aero', 'Paso de los Libres Aero']

entrerios_loc = ['Concordia Aero', 'Gualeguaychu Aero', 'Parana Aero']

formosa_locs = ['Formosa Aero', 'Las Lomitas Aero']

jujuy_locs = ['Jujuy Aero', 'Jujuy U N', 'La Quiaca Obs.']

lapampa_locs = ['General Pico Aero', 'Santa Rosa Aero', 'Victorica']

larioja_locs = ['Chamical Aero', 'Chepes', 'Chilecito Aero', 'La Rioja Aero']

mendoza_locs = ['Malargue Aero', 'Mendoza Aero', 'Mendoza Observatorio', 'San Carlos (mza)', 'San Martin (mza)', 'San Rafael Aero', 'Uspallata']

misiones_locs = ['Bernardo de Irigoyen Aero', 'Iguazu Aero', 'Obera Aero', 'Posadas Aero']

neuquen_locs = ['Chapelco Aero', 'Neuquen Aero']

rionegro_locs = ['Bariloche Aero', 'Cipolletti', 'El Bolson Aero', 'Maquinchao', 'Rio Colorado', 'San Antonio Oeste Aero', 'Viedma Aero']

salta_locs = ['Metan', 'Oran Aero', 'Rivadavia', 'Salta Aero', 'Tartagal Aero']

sanjuan_locs = ['Jachal', 'San Juan Aero']

sanluis_locs = ['San Luis Aero', 'Santa Rosa de Conlara Aero', 'Villa Reynolds Aero']

santacruz_locs = ['El Calafate Aero', 'Gobernador Gregores Aero', 'Perito Moreno Aero', 'Puerto Deseado Aero', 'Rio Gallegos Aero', 'San Julian Aero', 'Santa Cruz Aero']

santafe_locs = ['Ceres Aero', 'El Trebol Aero', 'Rafaela Aero', 'Reconquista Aero', 'Rosario Aero', 'Sauce Viejo Aero', 'Sunchales Aero', 'Venado Tuerto']

santiagodelestero_locs = ['Santiago del Estero Aero', 'Termas de Rio Hondo Aero']

tierradelfuego_locs = ['Rio Grande B.A.', 'Ushuaia Aero']

tucuman_locs = ['Tucuman Aero']



# HEADER



# MENU UBICACION

info = {
    'Buenos Aires': buenosaires_locs,
    'CABA': caba_locs,
    'Catamarca': catamarca_locs,
    'Chaco': chaco_locs,
    'Chubut': chubut_locs,
    'Cordoba': cordoba_locs,
    'Corrientes': corrientes_locs,
    'Entre Rios': entrerios_loc,
    'Formosa': formosa_locs,
    'Jujuy': jujuy_locs,
    'La Pampa': lapampa_locs,
    'La Rioja': larioja_locs,
    'Mendoza': mendoza_locs,
    'Misiones': misiones_locs,
    'Neuquen': neuquen_locs,
    'Rio Negro': rionegro_locs,
    'Salta': salta_locs,
    'San Juan': sanjuan_locs,
    'San Luis': sanluis_locs,
    'Santa Cruz': santacruz_locs,
    'Santa Fe': santafe_locs,
    'Santiago del Estero': santiagodelestero_locs,
    'Tierra del Fuego': tierradelfuego_locs,
    'Tucuman': tucuman_locs
}

######### DICCIONARIO CON LONGITUDES
dicc_longlat = {}
dicc_longlat['AZUL AERO'] = [-36.46 , -59.51]
dicc_longlat['BAHIA BLANCA AERO'] = [-38.71 , -62.27]
dicc_longlat['BENITO JUAREZ AERO'] = [-37.67 , -59.80]
dicc_longlat['BOLIVAR AERO'] = [-36.15 , -61.60]
dicc_longlat['CAMPO DE MAYO AERO'] = [-34.54 , -58.55]
dicc_longlat['CORONEL PRINGLES AERO'] = [-37.58 , -61.21]
dicc_longlat['CORONEL SUAREZ AERO'] = [-37.45 , -61.93]
dicc_longlat['DOLORES AERO'] = [-36.31 , -57.67]
dicc_longlat['EL PALOMAR AERO'] = [-34.3636 , -58.36]
dicc_longlat['EZEIZA AERO'] = [-34.8 , -58.54]
dicc_longlat['JUNIN AERO'] = [-33.14 , -68.47]
dicc_longlat['LA PLATA AERO'] = [-34.92 , -57.96]
dicc_longlat['LAS FLORES AERO'] = [-28.15 , -64.73]
dicc_longlat['MAR DEL PLATA AERO'] = [-38.00 , -57.53]
dicc_longlat['MARIANO MORENO AERO'] = [-34.46 , -58.92]
dicc_longlat['MERLO AERO'] = [-34.66 , -58.72]
dicc_longlat['MORON AERO'] = [-34.39 , -58.37]
dicc_longlat['NUEVE DE JULIO'] = [-31.66 , -68.39]
dicc_longlat['OLAVARRIA AERO'] = [-36.89 , -60.32]
dicc_longlat['PEHUAJO AERO'] = [-35.81 , -61.89]
dicc_longlat['PIGUE AERO'] = [-37.60 , -62.40]
dicc_longlat['PUNTA INDIO B.A.'] = [-35.26 , -57.23]
dicc_longlat['SAN FERNANDO'] = [-34.44 , -58.57]
dicc_longlat['SANTA TERESITA AERO'] = [-36.53 , -56.68]
dicc_longlat['TANDIL AERO'] = [-37.19 , -59.13]
dicc_longlat['TRENQUE LAUQUEN'] = [-36.01 , -62.40]
dicc_longlat['TRES ARROYOS'] = [-38.22 , -60.16]
dicc_longlat['VILLA GESELL AERO'] = [-37.26 , -56.97]
dicc_longlat['AEROPARQUE AERO'] = [-34.55 , -58.41]
dicc_longlat['BUENOS AIRES'] = [-34.60 , -58.38]
dicc_longlat['CATAMARCA AERO'] = [-28.46 , -65.78]
dicc_longlat['TINOGASTA'] = [-28.06 , -67.56]
dicc_longlat['PCIA. ROQUE SAENZ PE?A AERO'] = [-26.47 , -60.26]
dicc_longlat['RESISTENCIA AERO'] = [-27.46 , -58.98]
dicc_longlat['COMODORO RIVADAVIA AERO'] = [-45.43 , -67.31]
dicc_longlat['ESQUEL AERO'] = [-42.91 , -71.31]
dicc_longlat['PASO DE INDIOS'] = [-43.86 , -69.04]
dicc_longlat['PUERTO MADRYN AERO'] = [-42.76 , -65.03]
dicc_longlat['TRELEW AERO'] = [-43.24 , -65.30]
dicc_longlat['CORDOBA AERO'] = [-31.41 , -64.18]
dicc_longlat['CORDOBA OBSERVATORIO'] = [-31.41 , -64.18]
dicc_longlat['ESC.AVIACION MILITAR AERO'] = [-31.41 , -64.18]
dicc_longlat['LABOULAYE AERO'] = [-34.07 , -63.23]
dicc_longlat['MARCOS JUAREZ AERO'] = [-32.69 , -62.10]
dicc_longlat['PILAR OBS.'] = [-31.40 , -63.52]
dicc_longlat['RIO CUARTO AERO'] = [-33.13 , -64.34]
dicc_longlat['VILLA DOLORES AERO'] = [-31.94 , -65.18]
dicc_longlat['VILLA MARIA DEL RIO SECO'] = [-29.90 , -63.72]
dicc_longlat['CORRIENTES AERO'] = [-27.46 , -58.83]
dicc_longlat['ITUZAINGO'] = [-27.58 , -56.68]
dicc_longlat['MERCEDES AERO (CTES)'] = [-27.50 , -56.15]
dicc_longlat['MONTE CASEROS AERO'] = [-30.21 , -59.15]
dicc_longlat['PASO DE LOS LIBRES AERO'] = [-29.71 , -57.08]
dicc_longlat['CONCORDIA AERO'] = [-31.39 , -58.02]
dicc_longlat['GUALEGUAYCHU AERO'] = [-33.00 , -58.51]
dicc_longlat['PARANA AERO'] = [-31.73 , -60.52]
dicc_longlat['FORMOSA AERO'] = [-26.17 , -58.17]
dicc_longlat['LAS LOMITAS'] = [-24.70 , -60.59]
dicc_longlat['JUJUY AERO'] = [-24.18 , -65.30]
dicc_longlat['JUJUY U N'] = [-24.18 , -65.30]
dicc_longlat['LA QUIACA OBS.'] = [-22.06 , -65.35]
dicc_longlat['GENERAL PICO AERO'] = [-35.65 , -63.75]
dicc_longlat['SANTA ROSA AERO'] = [-36.61 , -64.28]
dicc_longlat['VICTORICA'] = [-23.71 , -62.95]
dicc_longlat['CHAMICAL AERO'] = [-30.36 , -66.31]
dicc_longlat['CHEPES'] = [-31.35 , -58.46]
dicc_longlat['CHILECITO AERO'] = [-29.16 , -67.49]
dicc_longlat['LA RIOJA AERO'] = [-29.41 , -66.85]
dicc_longlat['MALARGUE AERO'] = [-35.47 , -69.58]
dicc_longlat['MENDOZA AERO'] = [-32.53 , -68.49]
dicc_longlat['MENDOZA OBSERVATORIO'] = [-32.53 , -68.49]
dicc_longlat['SAN CARLOS (MZA)'] = [-69.02 , -69.04]
dicc_longlat['SAN MARTIN (MZA)'] = [-33.08 , -68.46]
dicc_longlat['SAN RAFAEL AERO '] = [-34.58 , -68.28]
dicc_longlat['USPALLATA'] = [-32.59 , -69.34]
dicc_longlat['BERNARDO DE IRIGOYEN AERO'] = [-32.10 , -61.09]
dicc_longlat['IGUAZU AERO'] = [-25.68 , -54.45]
dicc_longlat['OBERA AERO'] = [-27.29 , -55.07]
dicc_longlat['POSADAS AERO'] = [-27.36 , -55.89]
dicc_longlat['CHAPELCO AERO'] = [-40.23 , -71.26]
dicc_longlat['NEUQUEN AERO'] = [-38.57 , -68.03]
dicc_longlat['BARILOCHE AERO'] = [-41.13 , -71.30]
dicc_longlat['CIPOLLETTI'] = [-38.93 , -67.99]
dicc_longlat['EL BOLSON AERO'] = [-41.96 , -71.53]
dicc_longlat['MAQUINCHAO'] = [-41.25 , -68.73]
dicc_longlat['RIO COLORADO'] = [-22.27 , -65.41]
dicc_longlat['SAN ANTONIO OESTE AERO'] = [-40.44 , -64.58]
dicc_longlat['VIEDMA AERO'] = [-40.81 , -62.99]
dicc_longlat['METAN'] = [-27.06 , -64.83]
dicc_longlat['ORAN AERO'] = [-23.13 , -64.32]
dicc_longlat['RIVADAVIA'] = [-23.48 , -63.14]
dicc_longlat['SALTA AERO'] = [-24.78 , -65.41]
dicc_longlat['TARTAGAL AERO'] = [-22.51 , -63.80]
dicc_longlat['JACHAL'] = [-30.24 , -68.74]
dicc_longlat['SAN JUAN AERO'] = [-31.53 , -68.53]
dicc_longlat['SAN LUIS AERO'] = [-33.29 , -66.33]
dicc_longlat['SANTA ROSA DE CONLARA AERO'] = [-32.34 , -65.20]
dicc_longlat['VILLA REYNOLDS AERO'] = [-33.72 , -65.38]
dicc_longlat['EL CALAFATE AERO'] = [-50.20 , -72.16]
dicc_longlat['GOBERNADOR GREGORES AERO'] = [-48.45 , -70.14]
dicc_longlat['PERITO MORENO AERO'] = [-41.06 , -71.24]
dicc_longlat['PUERTO DESEADO AERO'] = [-47.75 , -65.89]
dicc_longlat['RIO GALLEGOS AERO'] = [-51.37 , -69.13]
dicc_longlat['SAN JULIAN AERO'] = [-49.30 , -67.72]
dicc_longlat['SANTA CRUZ AERO'] = [-50.07 , -68.19]
dicc_longlat['CERES AERO'] = [-29.88 , -61.94]
dicc_longlat['EL TREBOL'] = [-32.19 , -61.70]
dicc_longlat['RAFAELA AERO'] = [-31.25 , -61.48]
dicc_longlat['RECONQUISTA AERO'] = [-29.09 , -59.39]
dicc_longlat['ROSARIO AERO'] = [-32.95 , -60.66]
dicc_longlat['SAUCE VIEJO AERO'] = [-31.77 , -60.83]
dicc_longlat['SUNCHALES AERO'] = [-30.94 , -61.56]
dicc_longlat['VENADO TUERTO'] = [-33.74 , -61.96]
dicc_longlat['SANTIAGO DEL ESTERO AERO'] = [-27.47 , -64.15]
dicc_longlat['TERMAS DE RIO HONDO AERO'] = [-27.49 , -64.86]
dicc_longlat['RIO GRANDE B.A.'] = [-53.47 , -67.42]
dicc_longlat['USHUAIA AERO'] = [-54.81 , -68.31]
dicc_longlat['TUCUMAN AERO'] = [-26.82 , -65.22]



### FUNCION PARA CARGAR LA IMAGEN

def load_image(imagen):
    img = Image.open(imagen)
    return img

#### FUNCION PARA CARGAR MAPA
def find_lonlat(ciudad):
    return (dicc_longlat[ciudad])

######### SIDE BAR
with st.sidebar:
    selected = option_menu(
        menu_title='Menu principal',
        options=['Home', 'Información para el usuario.', 'Subí tu foto.', 'Carga manual.'],
    )

###########  HOME
if selected == 'Home':
    with st.container():
        st.subheader('Hola, somos 3 Data scientist de Argentina')
        st.title('Somos AirCon-Energy :bulb:')
        st.write('Esta aplicación te permite predecir el consumo eléctrico de un aire acondicionado en cualquier parte del territorio argentino.')


############# INFORMACION PARA EL USUARIO
if selected == 'Información para el usuario.':
    with st.container():
        st.subheader('Cómo usar paso a paso la aplicación.')
        st.text ('✅PASO 1: Elegí si queres subir una foto de la etiqueta de aire, o cargar los datos de forma manual.')
        st.text('✅PASO 2: Selecciona la provincia y ciudad.')
        st.text('✅PASO 3: Obtene el consumo aproximado que tendras con tu aire.')


        imagen_usuario = Image.open('img_usuario2.jpg')
        st.image(imagen_usuario, width=420)
        st.write(":heavy_minus_sign:" * 30)
        #st.markdown("""---""")
        imagen_edesur = Image.open('img_edesur.jpg')
        st.image(imagen_edesur, width=650)

########## UPLOAD YOUR PHOTO
if selected == 'Subí tu foto.':
    # adding "select" as the first and default choice
    provincia = st.selectbox('Selecciona tu provincia.', options=['Seleccioná tu provincia']+list(info.keys()))
    # display selectbox 2 if manufacturer is not "select"
    if provincia != 'Seleccioná tu provincia':
        ciudad = st.selectbox('Selecciona tu ciudad', options=info[provincia])
        ciu = ciudad.upper()
        lonlat = find_lonlat (ciu)
        df1 = pd.DataFrame(
        np.random.randn(500, 2) / [160, 160] + lonlat,
            columns=['lat', 'lon'])
        st.map(df1)
        inform1 = f'Ciudad: {ciudad}, Provincia:  {provincia},  Argentina.'
        st.info(inform1 , icon='🌎')

    imagen = st.file_uploader(label='Carga la foto adherida a tu aire acondicionado')


    if imagen is not None:
        st.image(load_image(imagen),width=250)

        #    api_url_image = 'http://127.0.0.1:8000/upload_image'
        #    res = requests.post(api_url_image, files={"file": imagen})
        #    prediction= res.json()
        dicc = detect_text(imagen)

        ERR = float((dicc['EER']).replace(',', '.'))
        CE = float((dicc['Cap_Refrig']).replace(',', '.'))

        list_ac_capacity = 0
        list_energy_efficiency = 0
        if 3.00 <= CE <= 4.0:
                list_ac_capacity = 1
        else:
                list_ac_capacity = 0

        if  3.00 < ERR <=3.20:
                list_energy_efficiency = 0
        else:
                list_energy_efficiency = 1


########## BOTON SUBMIT UPLOAD PHOTO

    if st.button('Calcular'):
        inform = f"Etiqueta de tu aire acondicionado --> Capacidad refrigeracion: {CE} kWh, Indice de eficiencia energética: {ERR}."
        st.info(inform, icon='📷')
        # st.info(inform1 , icon='🌎')
        params = dict(
        provincia_elegida= provincia,
        ciudad_elegida=ciudad,
        cap_kw = list_ac_capacity,
        indice_cap_energetica = list_energy_efficiency)

        energyac_api_url = 'http://127.0.0.1:8000/upload_image'
        response = requests.get(energyac_api_url, params=params)
        prediction = response.json()


        ######### GRAFICOS DE LA PREDICCION
        prediction= prediction['prediccion']
        lista_kw=[]
        for id_mes in ['11','12','1','2','3']:
            print(id_mes)
            hours_month=prediction[id_mes]['consumo']
            prediction1= (hours_month*CE)/ERR
            lista_kw.append(prediction1)
        dict_tmp={'1.Nov':lista_kw[0],'2.Dic':lista_kw[1],'3.En':lista_kw[2],'4.Feb':lista_kw[3],'5.Mar':lista_kw[3]}
        st.bar_chart(dict_tmp)
        for mes1,consum in zip(['Noviembre','Diciembre','Enero','Febrero','Marzo'],lista_kw):
            st.write(f"El consumo para {mes1} es de: " + str(round(consum)) + "KWh")
        st.subheader("Consumo promedio del dia por mes")
        fig=plt.figure(figsize=(20,10))
        plt.subplot(2,3,1)
        plt.stackplot(list(prediction['11']['horas_cons'].keys()),list(prediction['11']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Noviembre')
        plt.subplot(2,3,2)
        plt.stackplot(list(prediction['12']['horas_cons'].keys()),list(prediction['12']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Diciembre')
        plt.subplot(2,3,3)
        plt.stackplot(list(prediction['1']['horas_cons'].keys()),list(prediction['1']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Enero')
        plt.subplot(2,3,4)
        plt.stackplot(list(prediction['2']['horas_cons'].keys()),list(prediction['2']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Febrero')
        plt.subplot(2,3,5)
        plt.stackplot(list(prediction['3']['horas_cons'].keys()),list(prediction['3']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Marzo')
        plt.suptitle('Clima promedio por meses')
        st.pyplot(fig)



        #VISUALIZAR DATOS PREDICTION
        # bar_pred = dict((prediction['prediccion']))
        # sns.barplot(data=bar_pred, x='Mes', y="Consumo en KW")




##############   UPLOAD MANUALLY

if selected == 'Carga manual.':
    # adding "select" as the first and default choice
    provincia = st.selectbox('Selecciona tu provincia.', options=['Selecciona tu provincia']+list(info.keys()))
    # display selectbox 2 if manufacturer is not "select"
    if provincia != 'Selecciona tu provincia':
        ciudad = st.selectbox('Selecciona tu ciudad', options=info[provincia])
        ciu = ciudad.upper()
        lonlat = find_lonlat (ciu)
        df1 = pd.DataFrame(    np.random.randn(500, 2) / [160, 160] + lonlat,
            columns=['lat', 'lon'])
        st.map(df1)
        inform1 = f'Ciudad: {ciudad}, Provincia:  {provincia},  Argentina.'
        st.info(inform1 , icon='🌎')



    ##### BOTONES DE SELECCION

        ac_capacity_user = st.number_input('¿Cuál es la capacidad de tu aire acondicionado? (3.00 - 6.00)',min_value=3.0, max_value=6.0)

        energy_efficiency_user = st.number_input("Seleccioná la eficiencia energética de tu aire acondicionado",min_value=3.0, max_value=6.0)

        list_ac_capacity = 0
        list_energy_efficiency = 0

        if (3.0 <= ac_capacity_user < 4.5):
            list_ac_capacity = 1
        else:
            list_ac_capacity = 0

        if energy_efficiency_user < 3.20:
            list_energy_efficiency = 0
        else:
            list_energy_efficiency = 1

########## BOTON SUBMIT UPLOAD MANUALLY

    if st.button('Calcular'):
        params = dict(
        provincia_elegida= provincia,
        ciudad_elegida=ciudad,
        cap_kw = list_ac_capacity,
        indice_cap_energetica = list_energy_efficiency)


        energyac_api_url = 'http://127.0.0.1:8000/upload_manually'
        response = requests.get(energyac_api_url, params=params)
        prediction = response.json()


        ######### GRAFICOS DE LA PREDICCION
        prediction= prediction['prediccion']
        lista_kw=[]
        for id_mes in ['11','12','1','2','3']:
            hours_month=prediction[id_mes]['consumo']
            prediction1= (hours_month*ac_capacity_user)/energy_efficiency_user
            lista_kw.append(prediction1)
        #bar1=plt.bar(['Noviembre','Diciembre','Enero','Febrero','Marzo'],lista_kw)
        #st.pyplot(bar1)
        dict_tmp={'1.Nov':lista_kw[0],'2.Dic':lista_kw[1],'3.En':lista_kw[2],'4.Feb':lista_kw[3],'5.Mar':lista_kw[3]}
        st.bar_chart(dict_tmp)
        for mes1,consum in zip(['Noviembre','Diciembre','Enero','Febrero','Marzo'],lista_kw):
            st.write(f"El consumo para {mes1} es de: " + str(round(consum)) + "KWh")
        st.subheader("Consumo promedio del dia por mes")
        fig=plt.figure(figsize=(20,10))
        plt.subplot(2,3,1)
        plt.stackplot(list(prediction['11']['horas_cons'].keys()),list(prediction['11']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Noviembre')
        plt.subplot(2,3,2)
        plt.stackplot(list(prediction['12']['horas_cons'].keys()),list(prediction['12']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Diciembre')
        plt.subplot(2,3,3)
        plt.stackplot(list(prediction['1']['horas_cons'].keys()),list(prediction['1']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Enero')
        plt.subplot(2,3,4)
        plt.stackplot(list(prediction['2']['horas_cons'].keys()),list(prediction['2']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Febrero')
        plt.subplot(2,3,5)
        plt.stackplot(list(prediction['3']['horas_cons'].keys()),list(prediction['3']['horas_cons'].values()))
        plt.title('Consumo promedio por dia Marzo')
        plt.suptitle('Clima promedio por meses')
        st.pyplot(fig)
