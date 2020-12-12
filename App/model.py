





import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapstructure as m 
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import graphstructure as gr
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import selectionsort
from DISClib.Algorithms.Graphs import dfs
import datetime
assert config


#======================
#Estructura
#======================

def newanalizer():
    analyzer={'name':None, 'zones':None ,'global':{}}
    analyzer['global']['companies']=0
    analyzer['global']['taxis']=0
    analyzer['name']=m.newMap(numelements=50, maptype='PROBING', loadfactor=0.4, comparefunction=cmpids)
    analyzer['zones']=gr.newGraph(datastructure='ADJ_LIST', directed=True,size=78 ,comparefunction=cmpnumbers2)

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

#======================
#Consulta
#======================

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

def setride(A, B, hour1, hour2, graph):
    search=dfs.DepthFirstSearch(graph, A)
    path=dfs.pathTo(search, B)
    return path
#======================
#helper
#======================

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
        elif minutes in range(7,23):
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
            minutes= '0' + hours
        hour= hours + ':' +minutes
        return hour
    except:
        return None

#======================
#cmpfunctions
#======================

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