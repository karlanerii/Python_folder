# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:18:52 2021

@author: kneri
"""
#http://eldefe.com/mapa-colonias-delegacion-cuauhtemoc/ mapa colonias para comrobar calculos
import os
import pandas as pd
from simpledbf import Dbf5
import dbf
import numpy as np
import geopandas as gpd
from functools import reduce
import matplotlib.pyplot as plt
import seaborn as sns
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from adjustText import adjust_text
import matplotlib.ticker as ticker
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.colors
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from collision import *
from collision import Vector as v
import pandas as pd
import io
import folium
import folium.plugins
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Polygon
from shapely.geometry import Point
import numpy as np
import pyproj

#Llamar base de datos de python 
colonias = gpd.read_file("D:/Documentos/Banxico/Nota viviendas/DTA/coloniascdmx/coloniascdmx.shp") #llamar shape de colonias de CDMX 
colonias.crs
colonias = colonias.to_crs(epsg=5070) #4326 cambiar sistema se coordenadas para priorizar area

##Circulos
##############Hacerla función
transformer = pyproj.Transformer.from_crs("epsg:4326", "epsg:5070" )
transformer.transform( (19.43213),(-99.13339),) #pasar coordenadas del zocalo en 4326 a 5070

y, x = -379410.6607931329,-340005.2112485819 #localización del zocalito en 5070
polygonSides = 300 #número de circulos o lados del poligono

angles = np.linspace(0, 2 * np.pi, polygonSides, endpoint=False) #lineas

geo_total = []
for r in range(0, 21000, 1000):
    #r=r/100
    points_list = [(x + np.sin(a) * r,
                y + np.cos(a) * r)
               for a in angles] #hacer circulos a tanta distancia del zocalo
    df = pd.DataFrame(points_list) #pegar esas listas
    df=[Point(xy) for xy in zip(df[0], df[1])] #convertir esas distancias a puntos
    df[:3] #quedarme con el geo
    geo_df=gpd.GeoDataFrame(df, crs=5070, geometry=df) #pasar al mismo formato 
    geo_total.append(geo_df)

#separar cada circulo para graficar
for x in range(0,10,1):
    exec("string" + str(x) + " = 'hello'")

lista0=geo_total[0]
lista1=geo_total[1]
lista2=geo_total[2]
lista3=geo_total[3]
lista4=geo_total[4]
lista5=geo_total[5]
lista6=geo_total[6]
lista7=geo_total[7]
lista8=geo_total[8]
lista9=geo_total[9]
lista10=geo_total[10]
lista11=geo_total[11]
lista12=geo_total[12]
lista13=geo_total[13]
lista14=geo_total[14]
lista15=geo_total[15]
lista16=geo_total[16]
lista17=geo_total[17]
lista18=geo_total[18]
lista19=geo_total[19]
lista20=geo_total[20]

#revisar si existen valores en mi base
col =['CHAPULTEPEC']
def matcher(x):
    for i in col:
        if i.lower() in x.lower():
            return i
    else:
        return np.nan

colonias['Match'] = colonias['nombre'].apply(matcher) #imprimir aquellas colonias

#Crear algunas localizaciones para colonias conocidas
leyendas=colonias[  (colonias["nombre"]=="ROMA SUR I")
                  | (colonias["nombre"]=="POLANCO REFORMA POLANCO") 
                  | (colonias["nombre"]=="TLALPAN CENTRO")
                  | (colonias["nombre"]=="NONOALCO-TLATELOLCO (U HAB) ") 
                  | (colonias["nombre"]=="CENTRO IV") 
                  |  (colonias["nombre"]=="CIUDAD UNIVERSITARIA")
                  | (colonias["nombre"]=="LOMAS DE CHAPULTEPEC") 
                  | (colonias["nombre"]=="TACUBAYA")   
                  | (colonias["nombre"]=="VILLA COYOACAN")
                  | (colonias["nombre"]=="VILLA COYOACAN")                  
                  | (colonias["nombre"]=="MIXCOAC")                  
                  | (colonias["nombre"]=="JARDIN BALBUENA I")                  
                  | (colonias["nombre"]=="LINDAVISTA I")                  
                  | (colonias["nombre"]=="CALTONGO (BARR)")                  
                  | (colonias["nombre"]=="BUENAVISTA I")                  
                  | (colonias["nombre"]=="COLONIAL IZTAPALAPA (FRACC)")                  
                  | (colonias["nombre"]=="LOMAS DE PLATEROS (U HAB) I")                  
                  | (colonias["nombre"]=="TACUBA")                  
                  | (colonias["nombre"]=="LOMA DE LA PALMA")    
                  | (colonias["nombre"]=="CENTRO DE AZCAPOTZALCO")    
                  | (colonias["nombre"]=="SANTA FE")                  
                  | (colonias["nombre"]=="EL ROSARIO A (U HAB)")   
                  | (colonias["nombre"]=="VILLA XOCHIMILCO (U HAB)")
                  ]   

#Dejar nombre bien, sin errores etc, para proyección
#leyendas["nombre"]=np.where((leyendas["nombre"]=="JUAREZ"), "   Juárez", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="ROMA SUR I"), "Roma Sur", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="POLANCO REFORMA POLANCO"), "Polanco Reforma", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="TLALPAN CENTRO"), "Tlalpan Centro", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="NONOALCO-TLATELOLCO (U HAB)"), "Tlatelolco", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="CENTRO IV"), "Centro", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="CIUDAD UNIVERSITARIA"), "Ciudad Universitaria", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="LOMAS DE CHAPULTEPEC"), "Lomas de Chapultepec", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="TACUBAYA"), "Tacubaya", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="VILLA COYOACAN"), "Villa Coyoacán", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="MIXCOAC"), "Mixcoac", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="JARDIN BALBUENA I"), "Jardín de Balbuena", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="LINDAVISTA I") , "Lindavista", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="CALTONGO (BARR)"), "Caltongo Xochimilco", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="BUENAVISTA I") & (leyendas["cve_alc"]==7), "", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="BUENAVISTA I") , "Buenavista", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="COLONIAL IZTAPALAPA (FRACC)"), "Colonial Iztapalapa", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="LOMAS DE PLATEROS (U HAB) I"), "Plateros", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="TACUBA"), "Tacuba", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="LOMA DE LA PALMA"), "Loma de la Palma", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="CENTRO DE AZCAPOTZALCO"), "Azcapotzalco", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="SANTA FE"), "Santa Fé", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="EL ROSARIO A (U HAB)"), "El Rosario", leyendas["nombre"])                  
leyendas["nombre"]=np.where((leyendas["nombre"]=="VILLA XOCHIMILCO (U HAB)"), "Villa Xochimilco", leyendas["nombre"])                  
#colonias["leyendas"]=np.where((colonias["nombre"]==""), "", colonias["leyendas"])                  

leyendas["center"] = leyendas["geometry"].centroid #centro para poner las leyendas
za_points = leyendas.copy()
za_points.set_geometry("center", inplace = True)

#Grafíca de CDMX colonias
scala=900
alpha=.8
y, x = -379606.31,-340114.31 #localización del zocalito 
fontsize=42



fig, ax = plt.subplots(figsize=(60, 48)) #establecer mi marco
ax.axis("off") #eliminar mis ejes
colonias.plot(ax=ax,edgecolor="#C0C0C0", alpha=alpha, color="lightgray", linewidth=1)
lista0.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=3,  )  
lista1.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=.6)  
lista2.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=.7,)  
plt.text(x+scala*(1.7), y+scala*(-1.7),'2', fontsize=fontsize,)
lista3.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista4.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1)  
plt.text(x+scala*(3), y+scala*(-3),'4', fontsize=fontsize,)
lista5.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista6.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1)  
plt.text(x+scala*(4.9), y+scala*(-4.9),'6', fontsize=fontsize,)
lista7.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista8.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1)  
plt.text(x+scala*(6.3), y+scala*(-6.3),'8', fontsize=fontsize,)
lista9.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista10.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1)  
plt.text(x+scala*(7.9), y+scala*(-7.9),'10', fontsize=fontsize,)
lista11.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista12.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1) 
plt.text(x+scala*(9.4), y+scala*(-9.4),'12', fontsize=fontsize,)
lista13.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista14.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1) 
plt.text(x+scala*(11), y+scala*(-11),'14', fontsize=fontsize,)
lista15.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista16.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1)  
plt.text(x+scala*(12.7), y+scala*(-12.7),'16', fontsize=fontsize,)
lista17.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista18.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1) 
plt.text(x+scala*(14.3), y+scala*(-14.3),'18', fontsize=fontsize,)
lista19.plot(ax=ax,aspect=1, edgecolor="red", alpha=alpha, color="lightgray", linewidth=1)  
lista20.plot(ax=ax,aspect=1, edgecolor="blue", alpha=alpha, color="lightgray", linewidth=1)  
plt.text(x+scala*(15.8), y+scala*(-15.8),'20', fontsize=fontsize,)

#Añadir las leyendas
leyendas.plot( ax=ax,color = "#969696", edgecolor = "lightgrey", linewidth = 0.5)
texts = []
for x, y, label in zip(za_points.geometry.x, za_points.geometry.y, za_points["nombre"]):
    texts.append(plt.text(x, y, label, fontsize = 42))
    
plt.title("Circulos concéntricos del Zócalo de la CDMX (cada 1 km)",  fontsize=56,)











