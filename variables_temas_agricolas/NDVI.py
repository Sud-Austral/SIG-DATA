import ee
import geemap
import os
from datetime import datetime

Coleccion = "NOAA/CDR/AVHRR/NDVI/V5"
geometry = "users/leofabiop120/Chile/Malla_1km_y_Comuna_Chile_GCS"
estadistica = "MEAN"
nombreEstadistica = "MEDIA"
escala = 500
startDate = "2020-12-31"
rutaDescarga = "descarga"

def DescargaDatos():
    
    rango1 = []

    inicial = 435290
    final = 435311
    
    for i in range(1): # 84
        print(i + 1)
        
        Map = geemap.Map()
        landcoverColection = ee.ImageCollection(Coleccion)

        fecha_inicio = startDate
        fecha_final = "2021-01-01"
        # fecha_final = datetime.now().strftime("%Y-%m-%d")

        limites = ee.FeatureCollection(geometry)

        rango1 = inicial
        rango2 = final
        
        
        mallaFiltro = limites.filterMetadata("Parcela_ID", "greater_than", rango1) \
                                .filterMetadata("Parcela_ID", "less_than", rango2)

        out_dir = os.path.join(rutaDescarga)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        nombre_archivo = Coleccion.split("/")[1]

        # for band in landcoverColection.first().bandNames().getInfo():
        band = 'NDVI'
        print(f"Descargando los datos de {estadistica} correspondiente a la banda {band}")
        landcover = landcoverColection.select(band).filter(ee.Filter.date(fecha_inicio, fecha_final))
        out_dem_stats = os.path.join(out_dir, f'{nombre_archivo}_{nombreEstadistica}_{band}_{rango1+1}_{rango2-1}.csv')
        geemap.zonal_statistics(landcover, mallaFiltro, out_dem_stats, statistics_type=estadistica, scale=escala)
        # return nombre_archivo
        
        inicial = final - 1
        final += 10000

if __name__ == '__main__':
    DescargaDatos()

