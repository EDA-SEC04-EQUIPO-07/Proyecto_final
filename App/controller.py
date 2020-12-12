
import os
import config as cf
from App import model
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import liststructure as lt
import csv


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
    return analyzer



def topcompanies(N, mapa, category):
    return model.TopCompanies(N, mapa, category)

def setride(A, B, hour1, hour2, analyzer):
    graph=analyzer['zones']
    return model.setride(A, B, hour1, hour2, graph)
    