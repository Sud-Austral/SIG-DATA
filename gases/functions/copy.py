from shutil import copyfile

def copiar():
    copyfile('gases/functions/descarga/gases_CO.xlsx', 'gases/gases_CO_100.xlsx')

if __name__ == '__main__':
    copiar()
