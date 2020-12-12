import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit

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
    print('3- Imformacion de compañias.')

def submenuone():
    print('\n')
    print('\nTop de las primeras N compañias con respecto a la cantidad de taxis.')
    print('\nTop de las primeras N compañias con respecto a la cantidad de viajes realizados.')
#===================
#Funciones
#===================

def Optionone():
    return controller.init()

def Optiontwo(analyzer, file):
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

    elif inputs == '0':
        sys.exit(0)
    
    else:
        print('\nSeleción invalida.')

sys.exit(0)