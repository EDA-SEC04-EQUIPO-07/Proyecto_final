import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
import datetime

file='\\taxi-trips-wrvz-psew-subset-small.csv'

#===================
#Menus
#===================

def menu():
    print('\n')
    print('='*50)
    print('Bienvenidos.')
    print('1- Iniciar analizador.')
    print('2- Cargar datos.')
    print('3- Información de compañías.')
    print('5- Programar viaje.')

#===================
#Funciones
#===================

def Optionone():
    return controller.init()

def Optiontwo(analyzer, file):
    file='\\taxi-trips-wrvz-psew-subset-small.csv'
    print('\nIndique qué archivo desea cargar:\n>')
    print('1- Archivo small.')
    print('2- Archivo medium.')
    print('3- Archivo Large.')
    ent=input('Selecione una opcion:\n>')
    if ent == "1":
        file='\\taxi-trips-wrvz-psew-subset-small.csv'
    elif ent== "2":
        file='\\taxi-trips-wrvz-psew-subset-medium.csv'
    elif ent== "3":
        file='\\taxi-trips-wrvz-psew-subset-large.csv'

    controller.loadFile(cont, file)


def optionthree(analyzer):
    estadisticas=analyzer['global']
    print('\nHay un total de: ' + str(estadisticas['companies']) + ' compañias de taxis.')
    print('\nHay un total de: ' + str(estadisticas['taxis'])+ ' taxis.')
    N=int(input('\nIndique el numero de compañias que entran en el top de cantidad de taxis:\n>'))
    M=int(input('\nIndique el numero de compañias que entran en el top de cantidad de viajes:\n>'))
    mapa=cont['name']
    tops=controller.topcompanies(M, mapa, 'rides')
    tops_2=controller.topcompanies(N, mapa, 'taxis')
    print('Las ' + str(M)+' con las mayores cantidades de viajes son:\n')
    for i in tops:
        info=tops[i]
        name=info['Name']
        number=info['Number']
        print(str(i)+'- Compañia: '+ name+ ' total viajes: '+ str(number))
    print('\n'+'_'*50)
    print('\nLas ' + str(M)+' con las mayores cantidades de taxis son:\n')
    for i in tops_2:
        info=tops_2[i]
        name=info['Name']
        number=info['Number']
        print(str(i)+'- Compañia: '+ name+ ' total taxis: '+ str(number))

def optionfive(analyzer):
    vertexA=input('\nIngrese la zona de salida:\n>')
    vertexB=input('\nIngrese la zona de llegada:\n>')
    hour1=None
    hour2=None
    while hour1 is None and hour2 is None:
        try:
            print('\nLas hora de inicio y fin deben ser reportadas en el formato: 00:00 (24 horas)')
            hour1=input('\nIngrese la hora de inicio:\n>')
            hour2=input('\nIngrese la hora de finalización:\n>')
            hour1=controller.aproxhour(hour1)
            hour2=controller.aproxhour(hour2)
        except:
            hour1=None
            hour2=None
    validar=controller.setride(vertexA, vertexB, hour1, hour2, analyzer)
    if validar is None:
        print('\nHa ocurrido un error. Por favor verificar los datos.')
    else:
        (cadena, better)=validar
        duration=round(better['value'],4)
        print('\nLa ruta a seguir hasta la zona de llegada es:\n' + cadena)
        print('\nSe calculo que la mejor hora de partida es: '+ better['key'])
        print('\nEl viaje tiene una duracion de: '+str(duration)+' segundos.')

"""
Menu principal
"""

while True:
    menu()
    inputs=input('Selecione una opcion:\n>')
    if inputs == '1':
        cont=Optionone()

    elif inputs == '2':
        Optiontwo(cont, file)

    elif inputs == '3':
        optionthree(cont)
    
    elif inputs == '5':
        optionfive(cont)

    elif inputs == '0':
        sys.exit(0)
    
    else:
        print('\nSeleción invalida.')

sys.exit(0)