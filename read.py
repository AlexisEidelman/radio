# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:14:29 2015

@author: Alexis Eidelman
"""

import numpy as np
import pandas as pd
import os
import datetime
import networkx as nx
from bokeh.charts import Donut, show, output_file


path = "D:\data\\radio"
radio_list = ['FunRadio', 'LeMouv', 'Skyrock', 'Voltage']

def path_file(name, path):
    filename = 'Programmation-' + name + '-Fevrier-2015.csv'
    return os.path.join(path, filename)

def load(name, path=path):
    assert name in radio_list
    path_fil = path_file(name, path)
    sep = ','
    if name in ['FunRadio', 'Voltage']:
        sep = ';'
    tab = pd.read_csv(path_fil, sep=sep)
    return tab


def Skyrock():
    tab = load('Skyrock')
    
    for var in ['Artiste', 'Titre']:
        tab[var] = tab[var].str.lower()
        tab[var] = tab[var].str.rstrip()
        
    tab['Artiste'] = tab['Artiste'].str.split(' fea').str[0]    
    tab['Artiste'] =  tab['Artiste'].str.replace('arianna grande', 'ariana grande')
    tab['Artiste'] =  tab['Artiste'].str.replace('beyonce', 'beyoncé')
    tab['Artiste'] =  tab['Artiste'].str.replace('florida', 'flo rida')
    tab['Artiste'] =  tab['Artiste'].str.replace('i am', 'iam')
    tab['Artiste'] =  tab['Artiste'].str.replace('iggy azalea', 'iggy azaléa')
    tab['Artiste'] =  tab['Artiste'].str.replace('jay-z', 'jay z')    
    tab['Artiste'] =  tab['Artiste'].str.replace('ed sheraan', 'ed sheran')
    tab['Artiste'] =  tab['Artiste'].str.replace('ne-yo', 'ne yo')    
    tab['Artiste'] =  tab['Artiste'].str.replace('nelly furtado', 'nelly')


    tab['Titre'] =  tab['Titre'].str.replace('coco (clean version)', 'coco')    
    tab['Titre'] =  tab['Titre'].str.replace('laisse moi te dire (skyrock version)',
                                             'laisse moi te dire')


    tab['debut'] = pd.to_datetime(tab['start_ts'], unit='s')
    tab['fin'] = pd.to_datetime(tab['end_ts'], unit='s')
    tab['duree'] = tab['fin'] - tab['debut']
    tab.drop(['start_ts', 'end_ts'], axis=1, inplace=True)

    tab['duree_s'] = tab['duree']/ datetime.timedelta(0, 1)    
    
    return tab


def FunRadio():
    tab = load('FunRadio')
    tab['debut'] = pd.to_datetime(tab['Timestamp'], unit='s')
    tab.drop(['Timestamp', 'Date', 'Time'], axis=1, inplace=True)

    for var in ['Artiste', 'Titre']:
        tab[var] = tab[var].str.lower()
        tab[var] = tab[var].str.rstrip()

    return tab


def LeMouv():
    tab = load('LeMouv')
    tab['debut'] = pd.to_datetime(tab['startTime'], unit='s')
    tab['fin'] = pd.to_datetime(tab['endTime'], unit='s')
    tab['duree'] = tab['fin'] - tab['debut']
    tab['duree'] = tab['fin'] - tab['debut']
    tab.drop(['startTime', 'endTime', 'lien', 'lienYoutube'], axis=1,
             inplace=True)
    tab.rename(columns={'interpreteMorceau': 'Artiste', 'titreAlbum': 'Album',
                        'anneeEditionMusique': 'annee', 'titre': 'Titre'},
               inplace=True)

    for var in ['Artiste', 'Titre']:
        tab[var] = tab[var].str.lower()
        tab[var] = tab[var].str.rstrip()

    return tab


def Voltage():
    tab = load('Voltage')
    tab['debut'] = pd.to_datetime(tab['Timestamp'], unit='s')
    tab.drop(['Timestamp', 'Date', 'Temps'], axis=1, inplace=True)
    tab.rename(columns={'Chanson': 'Titre'}, inplace=True)

    for var in ['Artiste', 'Titre']:
        tab[var] = tab[var].str.lower()
        tab[var] = tab[var].str.rstrip()

    return tab


def some_stats(tab):
    print tab.Artiste.value_counts()
    print tab.Titre.value_counts()

    if 'duree' in tab.columns:
        tab['duree_s'] = tab['duree']/ datetime.timedelta(0, 1)
        res = tab.groupby('Artiste')['duree_s'].sum()
        res.sort()
        res.plot(kind='pie', figsize=(6, 6))


### TODO: faire des pie-chart
tab = Skyrock()

## on ne garde que les artistes diffusés
autre = tab.groupby('Artiste')['duree_s'].sum()
# sum(autre > 0.035*autre.sum()) == 10
select = autre[autre > 0.035*autre.sum()]
list_gros = select.index.tolist()
tab.loc[~tab['Artiste'].isin(list_gros), 'Artiste'] = "autre"
tab.loc[~tab['Artiste'].isin(list_gros), 'Titre'] = "autre"

val = tab.groupby(['Artiste','Titre']).aggregate('sum').reset_index()
gp = val.groupby(['Artiste'])

dico = dict()
liste = []
for name, group in gp:
    print name
    print group
    liste += [group['duree_s'].tolist()]
xxx


    
val = tab.groupby(['Artiste','Titre']).aggregate('sum')
val.reset_index(inplace=True)
autre = val.groupby('Artiste')['duree_s']


output_file("donut.html")
donut = Donut(liste)
show(donut)

res = tab.groupby('Artiste')['duree'].sum()
res.sort()
res /= datetime.timedelta(0, 1)
res.plot(kind='pie', figsize=(6, 6))
### TODO2: faire un graphe de connection entre les radios.


### compare deux radio
tab1 = Skyrock()
tab2 = FunRadio()
tab2 = LeMouv()

var = 'Artiste'
var = 'Titre'
values1 = set(tab1[var])
print len(values1)
values2 = set(tab2[var])
print len(values2)

commun = values2 &values1
print len(commun)
print len(values2 - values1)
print len(values1 - values2)

print values1 - values2
print values2 - values1


t1 = tab1[tab1[var].isin(commun)]
t2 = tab2[tab2[var].isin(commun)]

