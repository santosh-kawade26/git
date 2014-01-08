#!/usr/local/bin/python
from oauth2client import gce
from apiclient.discovery import build
import httplib2
credentials = gce.AppAssertionCredentials(
  scope='https://www.googleapis.com/auth/devstorage.read_write')
print credentials
http = credentials.authorize(httplib2.Http())
print http
#drive = build('drive', 'v2', http=http)
#print drive
result = service.activities().list(userId='me', collection='public').execute()
tasks = result.get('items', [])
for task in tasks:
  print task['title']


