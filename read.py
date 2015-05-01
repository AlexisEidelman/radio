# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 16:14:29 2015

@author: Alexis Eidelman
"""

import numpy as np
import pandas as pd
import os
import datetime



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
    tab['Artiste'] = tab['Artiste'].str.replace('Feat', 'feat')
    tab['Artiste'] = tab['Artiste'].str.replace('feat\.', 'feat')
    tab['Artiste'] = tab['Artiste'].str.rstrip()

    tab['debut'] = pd.to_datetime(tab['start_ts'], unit='s')
    tab['fin'] = pd.to_datetime(tab['end_ts'], unit='s')
    tab['duree'] = tab['fin'] - tab['debut']
    tab.drop(['start_ts', 'end_ts'], axis=1, inplace=True)
    return tab


def FunRadio():
    tab = load('FunRadio')
    tab['debut'] = pd.to_datetime(tab['Timestamp'], unit='s')
    tab.drop(['Timestamp', 'Date', 'Time'], axis=1, inplace=True)
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
    return tab


def Voltage():
    tab = load('Voltage')
    tab['debut'] = pd.to_datetime(tab['Timestamp'], unit='s')
    tab.drop(['Timestamp', 'Date', 'Temps'], axis=1, inplace=True)
    tab.rename(columns={'Chanson': 'Titre'}, inplace=True)
    return tab


def some_stats(tab):
    print tab.Artiste.value_counts()
    print tab.Titre.value_counts()

    if 'duree' in tab.columns:
        res = tab.groupby('Artiste')['duree'].sum()
        res.sort()
        res /= datetime.timedelta(0, 1)
        res.plot(kind='pie', figsize=(6, 6))
