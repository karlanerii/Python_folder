# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 18:38:41 2021
PROYECTO: NOTA DE VIVIENDA

OBJETIVO: Elaborar un mapa de densidad del empleo definido como 
         log(total de ocupados de x AGEB / area total de x AGEB)

BASES: DENEU-2019, Cartografia de correspondencia MANZANA-CP (elaborada por JPP)

@author: kneri karla.neri@banxico.org.mx
"""
##############################################################################
##  MAPAS DE DENSIDAD DEL EMPLEO POR KM2 
##############################################################################

import dbf
import folium
import folium.plugins
import geopandas as gpd
import io
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib.colors
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
import numpy as np
import os
import pandas as pd
import pyproj
import seaborn as sns
import shapely.ops as ops
import statistics

from adjustText import adjust_text
from collision import *
from collision import Vector as v
from functools import partial
from functools import reduce
from IPython import get_ipython
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable

from simpledbf import Dbf5
from pyproj import Geod
from shapely import wkt
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
from shapely.ops import transform
get_ipython().run_line_magic('matplotlib', 'inline')

#1. IMPORTAR: Llamar base de datos 
##############################################################################
denue = gpd.read_file("C:/Users/kneri/OneDrive/Documentos/2. Banxico/Nota viviendas/DTA/DENUE/denue_09_1119_shp/conjunto_de_datos/denue_inegi_09_.shp")
denue.columns= denue.columns.str.strip().str.lower()
manzanas = gpd.read_file("C:/Users/kneri/OneDrive/Documentos/2. Banxico/Nota viviendas/DTA/CP-manzana\df_manzanas_con_CP.shp") #llamar shape de colonias de CDMX 
manzanas.crs #observar formato del plano cartograf. de manzanas
manzanas = manzanas.to_crs(epsg=31370) #cambiar a algo para que cuadre lambert=31370 4326
#cdmx = gpd.read_file("E:/Database/DTA_original/INEGI/Cartografía/conjunto_de_datos/00ent.shp")

#2. CONSTRUCCIÓN BASE: Observar el número de trabajadores por manzana DENUE
##############################################################################
denue["pob_ocup"]=0
denue["pob_ocup"]=np.where((denue["per_ocu"]=="0 a 5 personas"), 3, denue["pob_ocup"])                  
denue["pob_ocup"]=np.where((denue["per_ocu"]=="6 a 10 personas"), 6, denue["pob_ocup"])                  
denue["pob_ocup"]=np.where((denue["per_ocu"]=="11 a 30 personas"), 11, denue["pob_ocup"])                  
denue["pob_ocup"]=np.where((denue["per_ocu"]=="31 a 50 personas"), 31, denue["pob_ocup"])                  
denue["pob_ocup"]=np.where((denue["per_ocu"]=="51 a 100 personas"), 51, denue["pob_ocup"])                  
denue["pob_ocup"]=np.where((denue["per_ocu"]=="101 a 250 personas"), 101, denue["pob_ocup"])                  
denue["pob_ocup"]=np.where((denue["per_ocu"]=="251 y más personas"), 251, denue["pob_ocup"])                  
denue.groupby(["pob_ocup", "per_ocu"]).size() #observar que asignación fue correcta
trabajadores=denue.groupby(["cve_ent", "cve_mun", "cve_loc", "ageb", "manzana"])["pob_ocup"].sum().reset_index() #sumar trab x mzna.

#3. CONSTRUCCIÓN BASE: Calcular area por manzana con shapefile de MANZANAS
############################################################################## 
#3.1 pegar cada manzana con su respectiva area
manzanas["area"]=manzanas.area
manzanas.groupby(["CVE_ENT", "CVE_MUN", ])["area"].sum().reset_index().round(0) #revisar que valores tengan sentido
manzanas = manzanas.to_crs(epsg=4326) #cambiar a algo para que cuadre lambert=31370 4326

#4. CONSTRUCCIÓN BASE: Consolidar una base del núm de trab x mnza con su areá y calcular densidad
############################################################################## 
dframe=pd.merge(manzanas, trabajadores, how='left', left_on=["CVE_MUN", "CVE_LOC", "CVE_AGEB", "CVE_MZA"], 
                                             right_on=["cve_mun", "cve_loc", "ageb", "manzana"  ])

#Suma de area y pob ocupada por AGEB                                                        
dframe['pobocup_a'] = (dframe.groupby(["cve_ent", "cve_mun", "cve_loc", "ageb"])['pob_ocup'].transform('sum'))
dframe['area_a'] = (dframe.groupby(["cve_ent", "cve_mun", "cve_loc", "ageb"])['area'].transform('sum'))

#Suma de area y pob ocupada por CP                                                        
dframe['pobocup_cp'] = (dframe.groupby(["cve_ent", "cve_mun", "d_cp"])['pob_ocup'].transform('sum'))
dframe['area_cp'] = (dframe.groupby(["cve_ent", "cve_mun", "d_cp",])['area'].transform('sum'))

#Calcular densidad del empleo POR AGEB
dframe["densidad"]=np.log(dframe["pobocup_a"]/(dframe["area_a"]/1000000))
dframe.hist(column='densidad')

a=dframe[dframe["pobocup_cp", "area_cp"]]
#5. REALIZAR MAPAS: Densidad por AGEB (total)
############################################################################## 
############################################################################## 

#Mapa total 
#5.1 Localización de algunos puntos de referencia
x, y = 19.43213, -99.13339 #localización del zocalito en 5070
x1, y1= 19.31877055361594, -99.18696118565649
x2, y2= 19.419811917252275, -99.1639566892932
x3, y3= 19.344164256810355, -99.19150112473187
x4, y4= 19.38588689957236, -99.22642632516367
x5, y5= 19.359469223241604, -99.27056859649568
x6, y6= 19.436382257008113, -99.19141720430864
x7, y7= 19.37463056268884, -99.08815370385929
x8, y8= 19.494089651750024, -99.16476503802058
fontsize=25 #tamaño letra

#5.2 Definir los rangos de la escala de colores del mapa para que se distingan zonas (normalizar)
var="densidad"

#5.3 Definir los colores que se utilizarán gráfica de colores y otras variables
norm = mcolors.TwoSlopeNorm(vmin=dframe[var].min(), vcenter=dframe[var].mean(), vmax=dframe[var].max()-2)
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [
                                      "#C21832", #rojo
                                      "#FFCD00", #amarillo
                                      "#000000", #azul 
                                      ])

#5.4 CAPA DEL MAPA
fig, ax = plt.subplots(figsize=(30, 20)) #establecer mi marco
dframe.plot(ax=ax, column=var, cmap=cmap, legend=True, alpha=1,
            norm=norm,  )
ax.axis("off") #eliminar mis ejes

#5.4 Añadir Leyendas
#plt.title("EMPLEO TOTAL POR KM2 \n Fuente:DENUE 2019", fontsize=fontsize, )
plt.text(y, x,'Zócalo', fontsize=fontsize, color="red")
plt.text(y2, x2,'Roma', fontsize=fontsize,color="white")
plt.text(y3, x3,'San Ángel', fontsize=fontsize,)
plt.text(y5, x5,'Lomas de Santa Fe', fontsize=fontsize-1,)
plt.text(y6, x6,'Polanco', fontsize=fontsize, color="white")
plt.text(y7, x7,'Central de Abastos', fontsize=fontsize,)

#5.4 Añadir flecha de norte 
x, y, arrow_length = 0.15, 0.95, 0.1
ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
            arrowprops=dict(facecolor='black', width=5, headwidth=15),
            ha='center', va='center', fontsize=20,
            xycoords=ax.transAxes)

#5.5 Añadir escala del mapa
ax.add_artist(ScaleBar(1, border_pad=1, label="5km", 
                       font_properties={ 'size': fontsize-1},
                       pad=1,))

# set an axis for the color bar
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.05)

# color bar
mappable = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cbar = fig.colorbar(mappable, cax=cax, orientation="horizontal")
cbar.ax.tick_params(labelsize=fontsize+1)


##borrar
#3. CONSTRUCCIÓN BASE: Calcular area por manzana con shapefile de MANZANAS
############################################################################## 
collap