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

from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapstructure as m 
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import graphstructure as gr
from DISClib.Algorithms.Graphs import dfs
from DISClib.ADT import stack as st
from DISClib.DataStructures import orderedmapstructure as om
from DISClib.Utils import error as error

import config
import datetime

assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

# Funciones para agregar informacion al grafo

def newanalizer():
    analyzer={'name':None, 'zones':None ,'infoDate':None ,'global':{}}
    analyzer['global']['companies']=0
    analyzer['global']['taxis']=0
    analyzer['name']=m.newMap(numelements=50, maptype='PROBING', loadfactor=0.4, comparefunction=cmpids)
    analyzer['zones']=gr.newGraph(datastructure='ADJ_LIST', directed=True,size=78 ,comparefunction=cmpnumbers2)
    analyzer['infoDate']=om.newMap(omaptype='RBT', comparefunction=cmpnumbers)

    return analyzer

#======================
#load
#======================

def addtrip(trip, analyzer):
    mapa=analyzer['name']
    estadisticas=analyzer['global']
    taxi=trip['taxi_id']
    company=trip['company']
    entry=m.get(mapa, company)
    if entry is None:
        value=newvalueC(company, taxi)
        m.put(mapa, company, value)
        estadisticas['companies']+=1
    else:
        value=me.getValue(entry)
    value['rides']+=1
    validar=validartaxi(taxi, value['taxis'])
    if validar:
        lt.addLast(value['taxis'], taxi)
        estadisticas['taxis']+=1

def loadgraph(trip, analyzer):
    graph=analyzer['zones']
    A=trip['pickup_community_area']
    B=trip['dropoff_community_area']
    duration=trip['trip_seconds']
    if A != '' and B != '' and duration != '':
        if A != B:
            duration=int(duration)
            time=trip['trip_start_timestamp']
            time=datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
            time=str(time.time())
            time=time[:5]
            addzone(A, graph)
            addzone(B, graph)
            addconection(A, B, duration, time,graph)

def addDate(trip, analyzer):
    Mapa= analyzer['infoDate']
    Date= trip['trip_start_timestamp']
    Date= datetime.datetime.strptime(Date, '%Y-%m-%dT%H:%M:%S.%f')
    Date= Date.date()
    TaxiID= trip['taxi_id']
    Total= trip['trip_total']
    Millas= trip['trip_miles']
    if Millas != "0" and Millas != "":
        if Total != "0" and Total != "":
            Total= float(Total)
            Millas= float(Millas)
            entry= om.get(Mapa, Date)
            if entry is None:
                value= newvalueD(Date, TaxiID, Millas, Total)
                om.put(Mapa, Date, value)
            else:    
                value= me.getValue(entry)
                Map=value['Taxis']
                addTaxi(TaxiID, Millas,Total, Map)

def addTaxi(TaxiID, Millas, Total, Mapa):
    entry= m.get(Mapa, TaxiID)
    if entry is None:
        value= newvalueT(TaxiID, Millas, Total)
        m.put(Mapa, TaxiID, value)
    else: 
        value= me.getValue(entry)
        value['Millas']+= Millas
        value['Total']+= Total
        value['Rides']+=1
            
def newvalueC(company, taxi):
    value={'name':company,'taxis':None, 'rides':1}
    value['taxis']=lt.newList(cmpfunction=cmpnumbers)
    return value

def addzone(vertex, graph):
    if not gr.containsVertex(graph, vertex):
        gr.insertVertex(graph, vertex)
        return graph

def addconection(A, B, duration, time, graph):
    edge=gr.getEdge(graph, A, B)
    if edge is None:
        value=newvalueConection(time, duration)
        gr.addEdge(graph, A, B, value)
    else:
        weight=edge['weight']
        addtime(time, weight, duration)

def newvalueConection(time, duration):
    value=m.newMap(numelements=24, maptype='PROBING', loadfactor=0.4, comparefunction=cmpnumbers2)
    addtime(time, value, duration)
    return value

def addtime(time, weight, duration):
    entry=m.get(weight, time)
    if entry is None:
        value=newvalueH(time, duration)
        m.put(weight, time, value)
    else:
        value=me.getValue(entry)
        average=value['duration']
        n=value['n']
        average=average*(n/n+1)+(1/n+1)*duration
        value['duration']=average

def newvalueH(time, duration):
    value={'time':time, 'duration':duration, 'n':1}
    return value

def newvalueD(Date, TaxiID, Millas, Total):
    value={'Date': Date, 'Taxis': None}
    value['Taxis']= m.newMap(maptype='PROBING',loadfactor=0.4, comparefunction=cmpids)
    addTaxi(TaxiID, Millas, Total, value['Taxis'])
    return value

def newvalueT(TaxiID, Millas, Total):
    value={'Taxi': TaxiID, 'Millas': Millas, 'Total': Total, 'Rides': 1}
    return value

# ==============================
# Funciones de consulta
# ==============================

def TopCompanies(N, mapa, category):
    top={}
    for i in range(1, N+1):
        top[i]={'Name':None, 'Number':0}
        i+=1
    keys=m.keySet(mapa)
    iterator=it.newIterator(keys)
    while it.hasNext(iterator):
        company=it.next(iterator)
        entry=m.get(mapa, company)
        value=me.getValue(entry)
        number=value[category]
        if category is 'taxis':
            number=lt.size(number)
        i=1
        info=top[i]
        if info['Name'] is None:
            for j in top:
                dicc=top[j]
                dicc['Name']=company
                dicc['Number']=number
        else:
            verificar=True
            while i in range(1, N+1) and verificar:
                info=top[i]
                if info['Number'] < number:
                    info['Name']=company
                    info['Number']=number
                    verificar=False
                i+=1
    return top

def bestTaxis(N, Date, analyzer):
    Mapa=analyzer['infoDate']
    entry=om.get(Mapa, Date)
    if entry is not None:
        value=me.getValue(entry)
        Map=value['Taxis']
        keys=m.keySet(Map)
        iterator=it.newIterator(keys)
        scores={}
        while it.hasNext(iterator):
            TaxiID=it.next(iterator)
            entryT=m.get(Map, TaxiID)
            value=me.getValue(entryT)
            score=calculateScore(value)
            scores[TaxiID]=score
        top=bestNdic(N, scores)
        return top
    else:
        return None

def bestTaxisRange(N, Date1, Date2, analyzer):
    Mapa=analyzer['infoDate']
    keys=om.keys(Mapa, Date1, Date2)
    print(keys)
    iterator=it.newIterator(keys)
    top={}
    while it.hasNext(iterator):
        Date=it.next(iterator)
        entry=om.get(Mapa, Date)
        value=me.getValue(entry)
        Map=value['Taxis']
        Taxis=m.keySet(Map)
        iteratorT=it.newIterator(Taxis)
        while it.hasNext(iteratorT):
            taxi=it.next(iteratorT)
            entry=m.get(Map, taxi)
            value=me.getValue(entry)
            milles=value['Millas']
            total=value['Total']
            rides=value['Rides']
            if taxi not in top:
                top[taxi]={}
                info=top[taxi]
                info['Millas']=milles
                info['Total']=total
                info['Rides']=rides
            else:
                info=top[taxi]
                info['Millas']+=milles
                info['Total']+=total
                info['Rides']+=rides
    print(top)
    for taxi in top:
        value=top[taxi]
        score=calculateScore(value)
        top[taxi]=score
    top=bestNdic(N, top)
    return top

def setride(A, B, hour1, hour2, graph):
    try:
        search=dfs.DepthFirstSearch(graph, A)
        if dfs.hasPathTo(search, B):
            path=dfs.pathTo(search, B)
            #data
            hours={}
            former=None
            cadena=None
            while not st.isEmpty(path):
                vertex=st.pop(path)
                if former is None:
                    former=vertex
                    cadena=str(vertex)
                else:
                    cadena+='-->'+str(vertex)
                    edge=gr.getEdge(graph, former, vertex)
                    weight=edge['weight']
                    keys=m.keySet(weight)
                    iterator=it.newIterator(keys)
                    while it.hasNext(iterator):
                        time=it.next(iterator)
                        if hour1 <= time:
                            if time <= hour2:
                                entry=m.get(weight, time)
                                value=me.getValue(entry)
                                duration=value['duration']
                                if time in hours:
                                    hours[time]+=duration
                                else:
                                    hours[time]=duration
                    former=vertex
            better=maxdic(hours)
            return (cadena,better)
    except:
        return None

# ==============================
# Funciones Helper
# ==============================

def validartaxi(taxi, lst):
    if lt.isPresent(lst, taxi) == 0:
        return True
    else:
        return False

def aproxhour(hour):
    """
    Aproxima los valores de ciertas horas.
    """
    try:
        hours=int(hour[:2])
        minutes=int(hour[3:])
        if minutes in range(0,8):
            minutes=00
        elif minutes in range(8,23):
            minutes=15
        elif minutes in range(23,38):
            minutes=30
        elif minutes in range(38,52):
            minutes=45
        else:
            minutes=00
            hours+=1
        minutes=str(minutes)
        hours=str(hours)
        if len(minutes) == 1:
            minutes= '0' + minutes
        if len(hours) == 1:
            hours= '0' + hours
        hour= hours + ':' +minutes
        return hour
    except:
        return None

def maxdic(dic):
    higer={'key':None, 'value':None}
    for key in dic:
        if higer['key'] is None:
            higer['key']=key
            higer['value']=dic[key]
        elif higer['value'] < dic[key]:
            higer['key']=key
            higer['value']=dic[key]
    return higer

def calculateScore(value):
    miles=value['Millas']
    total=value['Total']
    ride=value['Rides']
    score=miles/total
    score=score*ride
    return score

def bestNdic(N, dic):
    top={}
    for i in range(1, N+1):
        top[i]={'id':None, 'score':None}
    for Id in dic:
        score=dic[Id]
        i=1
        if top[i]['score'] == None:
            for i in top:
                top[i]['id']=Id
                top[i]['score']=score
        else:
            verificar=True
            while i in range(1,N+1) and verificar:
                info=top[i]
                if info['score'] < score:
                    info['id']=Id
                    info['score']=score
                    verificar=False
                i+=1
    return top

# ==============================
# Funciones de Comparacion
# ==============================

def cmpids(id1,id2):
    id2=id2['key']
    if id1 > id2:
        return 1
    elif id1==id2:
        return 0
    else:
        return -1

def cmpnumbers(n1, n2):
    if n1 < n2:
        return 1
    elif n1==n2:
        return 0
    else:
        return -1

def cmpnumbersl(n1, n2):
    if n1 < n2:
        return 1
    elif n1==n2:
        return 0
    else:
        return -1

def cmpnumbers2(n1, n2):
    n2=n2['key']
    if n1 < n2:
        return 1
    elif n1==n2:
        return 0
    else:
        return -1
