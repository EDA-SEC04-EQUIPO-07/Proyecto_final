





import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapstructure as m 
from DISClib.DataStructures import mapentry as me
from DISClib.Utils import error as error
from DISClib.Algorithms.Sorting import selectionsort
import datetime
assert config


#======================
#Estructura
#======================

def newanalizer():
    analyzer={'name':None, 'rides':None, 'taxis':None,  'global':{'companies':0, 'taxis':0}}

    analyzer['name']=m.newMap(numelements=50, maptype='PROBING', loadfactor=0.4, comparefunction=cmpids)
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
 
def newvalueC(company, taxi):
    value={'name':company,'taxis':None, 'rides':1}
    value['taxis']=lt.newList(cmpfunction=cmpnumbers)
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
                print('hola')
                info=top[i]
                if info['Number'] < number:
                    info['Name']=company
                    info['Number']=number
                    verificar=False
                i+=1
    return top


#======================
#helper
#======================

def validartaxi(taxi, lst):
    if lt.isPresent(lst, taxi) == 0:
        return True
    else:
        return False

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