#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:43:05 2020

@author: Colin
"""

import os
path = os.path.abspath(os.getcwd())
list_subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]
print(list_subfolders_with_paths)