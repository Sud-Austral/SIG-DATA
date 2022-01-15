from shutil import copyfile

def copiar():
    copyfile('gases/functions/descarga/gases_CO.xlsx', 'gases/gases_CO_100.xlsx')
    copyfile('gases/functions/descarga/gases_AI.xlsx', 'gases/gases_AI.xlsx')
    copyfile('gases/functions/descarga/gases_HCHO.xlsx', 'gases/gases_HCHO.xlsx')
    copyfile('gases/functions/descarga/gases_NO2.xlsx', 'gases/gases_NO2.xlsx')
    copyfile('gases/functions/descarga/gases_SO2.xlsx', 'gases/gases_SO2.xlsx')
    copyfile('gases/functions/descarga/gases_O3.xlsx', 'gases/gases_O3.xlsx')

if __name__ == '__main__':
    copiar()
