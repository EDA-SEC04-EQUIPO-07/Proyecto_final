"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
import datetime

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""


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
    print('4- Mejores Taxis')
    print('5- Programar viaje.')

def submenuO2():
    print('\n   Indique qué archivo desea cargar.')
    print('   1- Archivo small.')
    print('   2- Archivo medium.')
    print('   3- Archivo Large.')
    ent=input('   Selecione una opcion:\n   >')
    return ent

def submenuO4():
    print('\nOpciones :')
    print('1- Buscar el mejor taxi en una fecha.')
    print('2- Buscar el mejor taxi en un rango de fechas.')
    ent=input('Selecione una opcion:\n>')
    return ent

#===================
#Funciones
#===================

def Optionone():
    return controller.init()

def Optiontwo():
    ent=None
    while ent is None:
        ent=submenuO2()
        if ent == "1":
            file='\\taxi-trips-wrvz-psew-subset-small.csv'
        elif ent== "2":
            file='\\taxi-trips-wrvz-psew-subset-medium.csv'
        elif ent== "3":
            file='\\taxi-trips-wrvz-psew-subset-large.csv'
        else:
            ent=None

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
    print('\nLas ' + str(N)+' con las mayores cantidades de taxis son:\n')
    for i in tops_2:
        info=tops_2[i]
        name=info['Name']
        number=info['Number']
        print(str(i)+'- Compañia: '+ name+ ' total taxis: '+ str(number))

def optionfour():
    option=None
    while option is None:
        option=submenuO4()
        if option == '1':
            Date=input('\nIngrese la fecha de busqueda, formato YYYY-mm-dd:\n>')
            N= None
            while N is None:
                N=input('\nIndique el numero del top:\n>')
                try:
                    N=int(N)
                except:
                    N=None
            Date=datetime.datetime.strptime(Date, '%Y-%m-%d')
            Date=Date.date()
            top=controller.bestTaxis(N, Date, cont)
            if top is not None:
                print('\nLos mejores taxis para la fehca dada son: ')
                i=1
                for taxi in top:
                    score=round(top[taxi],2)
                    print( str(i) + ' El taxi: '+ taxi + ' puntuacion de :'+ str(score) )
            else:
                print('Verifique los datos dados.')
        elif option== '2':
            Date1=input('\nIngrese la fecha inicial de busqueda; formato YYYY-mm-dd :\n>')
            Date2=input('\nIngrese la fecha inicial de busqueda; formato YYYY-mm-dd :\n>')
            N= None
            while N is None:
                N=input('\nIndique el numero del top:\n>')
                try:
                    N=int(N)
                except:
                    N=None
            Date1=datetime.datetime.strptime(Date1, '%Y-%m-%d')
            Date1=Date1.date()
            Date2=datetime.datetime.strptime(Date2, '%Y-%m-%d')
            Date2=Date2.date()
            top=controller.bestTaxisRange(N, Date1, Date2, cont)
            if top is not None:
                print('\nLos mejores taxis para la fehca dada son: ')
                i=1
                for taxi in top:
                    score=round(top[taxi],2)
                    print( str(i) + ' El taxi: '+ taxi + ' puntuacion de :'+ str(score) )
            else:
                print('Verifique los datos dados.')

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
        Optiontwo()

    elif inputs == '3':
        optionthree(cont)
    
    elif inputs == '4':
        optionfour()
    
    elif inputs == '5':
        optionfive(cont)

    elif inputs == '0':
        sys.exit(0)
    
    else:
        print('\nSeleción invalida.')

sys.exit(0)