#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:47:57 2020

@author: Colin
"""

from oauth2client.service_account import ServiceAccountCredentials
import gspread

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./oauth/client_secret.json', scope)
client = gspread.authorize(creds)