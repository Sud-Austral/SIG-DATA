import pandas as pd
import numpy as np
import ee
import glob
import geemap
from datetime import timedelta
import datetime


def descargaNO2():

    file = 'data/ciudades/*.json'
    files = glob.glob(file)

    filenames = np.array(files)

    Map = geemap.Map()

    dfHistorico = pd.read_csv('gases/functions/descarga/gases_NO2.csv')
    maxDate = dfHistorico['Fecha'].max().replace('-','/')

    date_object = datetime.datetime.strptime(maxDate, '%Y/%m/%d')

    currentDate = datetime.datetime.now() - date_object
    difference = currentDate.days
    
    startDate = datetime.datetime.now() - timedelta(days=difference - 1)

    salida = []

    # ¡¡¡IMPORTANTE!!!
    # CAMBIAR NÚMERO '1' DEL PRIMER BUCLE, SE UTILIZA SOLAMENTE EN EL PERÍODO DE PRUEBA, SUSTITUIR POR VARIABLE 'difference'

    for i in range(1):
        salida = []
        
        for j in filenames:
            fechaInicial = startDate + timedelta(days=i)
            fechaFinal = startDate + timedelta(days=(i + 1))


            fechaI = fechaInicial.strftime('%Y-%m-%d')
            fechaF = fechaFinal.strftime('%Y-%m-%d')

            dataset = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_NO2') \
                          .filter(ee.Filter.date(fechaI, fechaF))

            col_final = dataset.mean().select('NO2_column_number_density')

            geom = geemap.geojson_to_ee(j)
            geom = geom.select('id_ciud_N', 'NO2_column_number_density')

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

        
        df = pd.DataFrame(salida)
        cant = len(df.columns)

        if(cant == 3):
            # df.to_excel('descarga/' + str(fechaI) + '.xlsx', index=False)
            finalDf = pd.concat([dfHistorico, df])
            finalDf.to_csv('gases/functions/descarga/gases_NO2.csv', index=False)
            print('Datos actualizados: ' + str(fechaI))
        else:
            print('Sin información: ' + str(fechaI))

if __name__ == '__main__':
    descargaNO2()
            