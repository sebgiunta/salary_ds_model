# -*- coding: utf-8 -*-
"""
Created on Tue May 17 09:10:51 2022

@author: sebgi
"""

import glassdoor_scraper as gs
import pandas as pd

df = gs.get_jobs(5, False)