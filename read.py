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
tab = pd.read_csv(os.path.join(path, "Skyrock-2015-02.csv"))

tab.Artiste.value_counts()
tab.Titre.value_counts()

## correction
tab['Artiste'] = tab['Artiste'].str.replace('Feat','feat')
tab['Artiste'] = tab['Artiste'].str.replace('feat\.','feat')
tab['Artiste'] = tab['Artiste'].str.rstrip()

tab['debut'] = pd.to_datetime(tab['start_ts'], unit='s')
tab['fin'] = pd.to_datetime(tab['end_ts'], unit='s')
tab['duree'] = tab['fin'] - tab['debut']
res = tab.groupby('Artiste')['duree'].sum()

