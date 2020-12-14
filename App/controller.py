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

import os
import config as cf
from App import model
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import liststructure as lt
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

#====================
#Load
#====================

def init():
    analyzer=model.newanalizer()
    return analyzer

def loadFile(analyzer, tripfile):
    """
    """
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile, encoding="utf-8"),
                                delimiter=",")
    for trip in input_file:
        model.addtrip(trip, analyzer)
        model.loadgraph(trip, analyzer)
        model.addDate(trip, analyzer)
    return analyzer

#====================
#consulta
#====================

def topcompanies(N, mapa, category):
    return model.TopCompanies(N, mapa, category)

def setride(A, B, hour1, hour2, analyzer):
    graph=analyzer['zones']
    return model.setride(A, B, hour1, hour2, graph)

def bestTaxis(N, Date, analyzer):
    return model.bestTaxis(N, Date, analyzer)

def bestTaxisRange(N, date1, date2, analyzer):
    return model.bestTaxisRange(N, date1, date2, analyzer)
    
#====================
#Helper
#====================

def aproxhour(hour):
    return model.aproxhour(hour)