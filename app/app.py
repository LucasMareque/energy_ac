import streamlit as st
import pandas as pd
import numpy as np
from fastapi import FastAPI, File, UploadFile, Form
from energy_ac.gcloud import detect_text
import os
import pickle


app = FastAPI()



def query_station(provincia,ciudad):
    os.chdir('/home/lucas/code/LucasMareque/energy_ac/raw_data/')
    data = pd.read_excel('weatherdata-arg-estaciones.xlsx')
    station = data[(data["PROVINCIA"]==provincia) & (data["NOMBRE"]==ciudad)]['NRO'].max()
    data1 = pd.read_csv('data_arg_escalado.csv')
    hour = data1[data1["estacion"]==station]['Hour']
    temp = data1[data1["estacion"]==station]['temp_C']
    hum = data1[data1["estacion"]==station]['humidity']
    st_term = data1[data1["estacion"]==station]['FeelsLikeC']
    #crear df de arg
    data_arg=pd.concat([data1[data1["estacion"]==station]['datetime'],hour,temp,hum,st_term], axis=1)
    #data_arg=data_arg.drop(columns='datetime')
    return data_arg

#chequear con lo que hace martin
def eer_class(eer):
    if eer > 3.20:
        prim_ac_star_a = 1.0
        prim_ac_star_b = 0.0
    elif  3.00 < eer <= 3.20:
        prim_ac_star_a = 0.0
        prim_ac_star_b = 1.0

    return(prim_ac_star_a, prim_ac_star_b)

#chequear con lo que hace martin
def prim_ac(clase):
    if clase >= 3:
        prim_ac_12 = 1.0
        prim_ac_18 = 0.0
    elif clase >= 6:
        prim_ac_12 = 0.0
        prim_ac_18 = 1.0
    return(prim_ac_12, prim_ac_18)


def predicted(data_arg):

    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    ##prediccion
    predictions = model.predict(data_arg)
    return predictions



@app.get('/predict')
async def index(provincia_elegida,
        ciudad_elegida,
        cap_kw,
        indice_cap_energetica):
    return {'funcionando': 'hola'}


@app.get('/upload_image')
async def upload_image(provincia_elegida: str,
                        ciudad_elegida: str,
                        cap_kw: int,
                          indice_cap_energetica: int):
    provincia_elegida = provincia_elegida.upper()
    ciudad_elegida = ciudad_elegida.upper()
    c1 = query_station(provincia_elegida, ciudad_elegida)
    c1[['primary AC tonnage_12k','primary AC tonnage_18k', 'primary AC star rating_A','primary AC star rating_B']] = [cap_kw,1-cap_kw, indice_cap_energetica, 1-indice_cap_energetica]
    print(cap_kw, 'aca va la lista de prueba')
    #c2 = prim_ac(float(cap_kw))
    #c3 = eer_class(float(indice_cap_energetica))
    #X_predict=data_arg[[c1[0],c1[1],c1[2],c1[3],c2[0],c2[1],c3[0],c3[1]]]
    c1['datetime']=pd.to_datetime(c1['datetime'],format="%m/%d/%Y")
    c1['month']=c1['datetime'].dt.month
    c1=c1.drop(columns=['datetime'])
    predicciones={}
    for i in [11,12,1,2,3]:
        prueba_tmp=c1
        prueba_tmp=prueba_tmp[prueba_tmp['month']==i]
        prueba_tmp=prueba_tmp.drop(columns=['month'])
        total_horas=0
        list_consumo=[]
        prediccion= np.where(prueba_tmp['temp_C'] > -2.0, (predicted(pd.DataFrame(prueba_tmp))+20)/60 , 0)
        prediccion=prediccion.reshape(-1, 24)
        consumo_hora= prediccion.mean(axis=0)
        dict_consumo={}
        for hour,cons in zip(range(0,24),consumo_hora):
            dict_consumo[str(hour)]=float(cons)
        predicciones[str(i)]={'consumo':float(prediccion.sum()),'horas_cons':dict_consumo}
    return {'prediccion': dict(predicciones)}






@app.get('/upload_manually')
async def upload_manually(provincia_elegida: str,
                          ciudad_elegida: str,
                          cap_kw: int,
                          indice_cap_energetica: int):
    provincia_elegida = provincia_elegida.upper()
    ciudad_elegida = ciudad_elegida.upper()
    c1 = query_station(provincia_elegida, ciudad_elegida)
    c1[['primary AC tonnage_12k','primary AC tonnage_18k', 'primary AC star rating_A','primary AC star rating_B']] = [cap_kw,1-cap_kw, indice_cap_energetica, 1-indice_cap_energetica]
    print(cap_kw, 'aca va la lista de prueba')

    c1['datetime']=pd.to_datetime(c1['datetime'],format="%m/%d/%Y")
    c1['month']=c1['datetime'].dt.month
    c1=c1.drop(columns=['datetime'])
    predicciones={}
    for i in [11,12,1,2,3]:
        prueba_tmp=c1
        prueba_tmp=prueba_tmp[prueba_tmp['month']==i]
        prueba_tmp=prueba_tmp.drop(columns=['month'])
        total_horas=0
        list_consumo=[]
        prediccion= np.where(prueba_tmp['temp_C'] > -2.0, (predicted(pd.DataFrame(prueba_tmp))+20)/60 , 0)
        prediccion=prediccion.reshape(-1, 24)
        consumo_hora= prediccion.mean(axis=0)
        dict_consumo={}
        for hour,cons in zip(range(0,24),consumo_hora):
            dict_consumo[str(hour)]=float(cons)
        predicciones[str(i)]={'consumo':float(prediccion.sum()),'horas_cons':dict_consumo}
    return {'prediccion': dict(predicciones)}







# data_arg = query_station(ciudad_elegida,localidad_elegida)
# data_arg.append(cap_kw)
# data_arg.append(indice_cap_energetica)
# X_predict = []
# prediction(x_predict)
# return {'funcionando1': data_arg}






#@app.get('/predict')
#def predict(loc):
#    query_station(province,city):
 #       X_predict = ()
  #      y.pipe.predict(X_predict)
   #     return ()
