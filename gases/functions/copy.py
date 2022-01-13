from shutil import copyfile

def copiar():
    copyfile('gases/functions/descarga/gases_CO.xlsx', 'gases/')

if __name__ == '__main__':
    copiar()
