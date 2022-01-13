import pandas as pd
import numpy as np
import ee
import glob
import geemap
from datetime import timedelta
import datetime
from os import remove


def descarga():

    datoExistente = 0

    file = 'gases/functions/data/ciudades/*.json'
    files = glob.glob(file)

    filenames = np.array(files)
    # print('CANTIDAD: ' + str(len(filenames)))
    Map = geemap.Map()

    dfHistorico = pd.read_csv('gases/functions/descarga/gases_AI.csv')
    maxDate = dfHistorico['Fecha'].max().replace('-','/')

    date_object = datetime.datetime.strptime(maxDate, '%Y/%m/%d')

    currentDate = datetime.datetime.now() - date_object
    difference = currentDate.days
    
    startDate = datetime.datetime.now() - timedelta(days=difference - 1)

    # GLOBAL
    fechaInicial = startDate
    fechaFinal = startDate

    fechaI = fechaInicial.strftime('%Y-%m-%d')
    fechaF = fechaFinal.strftime('%Y-%m-%d')

    # ¡¡¡IMPORTANTE!!!
    # CAMBIAR NÚMERO '1' DEL PRIMER BUCLE, SE UTILIZA SOLAMENTE EN EL PERÍODO DE PRUEBA, SUSTITUIR POR VARIABLE 'difference'

    for i in range(difference):

        salida = []
        
        for j in filenames:
            try:
                fechaInicial = startDate + timedelta(days=i)
                fechaFinal = startDate + timedelta(days=(i + 1))

                fechaI = fechaInicial.strftime('%Y-%m-%d')
                fechaF = fechaFinal.strftime('%Y-%m-%d')

                dataset = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_AER_AI') \
                            .filter(ee.Filter.date(fechaI, fechaF))

                col_final = dataset.mean().select('absorbing_aerosol_index')

                geom = geemap.geojson_to_ee(j)
                geom = geom.select('id_ciud_N', 'absorbing_aerosol_index')

                Datos_Mediana = col_final.reduceRegions (
                collection = geom,
                crs = 'EPSG:4326',
                reducer = ee.Reducer.mean(),
                scale = 500

                )

                # Asegurarse de que sea un solo valor
                diccionarioParcial = Datos_Mediana.getInfo()['features'][0]['properties']
                diccionarioParcial['Fecha'] = fechaI

                # print(diccionarioParcial)
                salida.append(diccionarioParcial.copy())

                datoExistente = 1

            except:
                datoExistente = 0
                print('Sin información: ' + str(fechaI))

        if(datoExistente == 1):
            df = pd.DataFrame(salida)
            cant = len(df.columns)
            if(cant >= 3):
                df.to_csv('gases/functions/temp/' + str(fechaI) + '.csv', index=False)
                print('Datos actualizados: ' + str(fechaI))
            else:
                print('Sin información: ' + str(fechaI))
        else:
            pass

def consolidar():

    fileDelete = 'gases/functions/temp/*.csv'
    fileDelete = glob.glob(fileDelete)

    filenamesDelete = np.array(fileDelete)
    actualizaDF = pd.concat([pd.read_csv(f) for f in filenamesDelete])

    for a in filenamesDelete:
        remove(a)

    dfHistorico = pd.read_csv('gases/functions/descarga/gases_AI.csv')
    finalDf = pd.concat([dfHistorico, actualizaDF])

    finalDf.to_excel('gases/functions/descarga/gases_AI.xlsx', index=False)

if __name__ == '__main__':
    descarga()
    consolidar()

