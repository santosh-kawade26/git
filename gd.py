#!/usr/bin/python
#@author San
import httplib2
import pprint
import sys
from apiclient import errors
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

# Email of the Service Account.
SERVICE_ACCOUNT_EMAIL = '568380262348-411m4shg87sn2tcn7utlh9uaomilaekf@developer.gserviceaccount.com'

# Path to the Service Account's Private Key file.
SERVICE_ACCOUNT_PKCS12_FILE_PATH = '/Users/santoshk/Downloads/p1.p12'

def createDriveService():
  """Builds and returns a Drive service object authorized with the given service account.

  Returns:
    Drive service object.
  """
  f = file(SERVICE_ACCOUNT_PKCS12_FILE_PATH, 'rb')
  key = f.read()
  f.close()

  credentials = SignedJwtAssertionCredentials(SERVICE_ACCOUNT_EMAIL, key,
      scope='https://www.googleapis.com/auth/drive')
  http = httplib2.Http()
  print http
  http = credentials.authorize(http)

  return build('drive', 'v2', http=http)
  #print service

# Download files
 
def download_file(service, drive_file):
  """Download a file's content.

  Args:
    service: Drive API service instance.
    drive_file: Drive File instance.

  Returns:
    File's content if successful, None otherwise.
  """
  print 'In download files'
  #files = drive_file.get['items']
  #print files 
  #download_url = file['exportLinks']['application/pdf']
  download_url = drive_file.get('downloadUrl')
  print '################## Download URL #######################'
  print download_url
  if download_url:
    print 'Hiiiiiiiiiiiiiiiii' 
    resp, content = service._http.request(download_url)
    if resp.status == 200:
      #print 'Status: %s' % resp
      f = resp['content-disposition']
      date = drive_file.get('userPermission')
      print date
      if (drive_file.get('mimeType') == 'application/zip'):
      	print f
      #MIME type: application/zip
      	print '#######################################################file################################################'
      	title = drive_file.get('title')
      	print title
      	title = str(title)
      	print title
      	str1 = "quickoffice-chrome-0.0.0."
      	n = title.find(str1)
      	print n
      	#if (title.find("quickoffice-chrome.0.0.0.") != -1):
      		
      #title = content['filename']
      print title
      path = '/tmp/'+title
      file = open(path, 'wb')
      file.write(content)
      #print content
      return content
    else:
      print 'An error occurred: %s' % resp
      return None
  else:
    # The file doesn't have any content stored on Drive.
    return None

# Get files
def print_file(service, file_id):
  """Print a file's metadata.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to print metadata for.
  """
  print 'In print_file'
  try:
    file = service.files().get(fileId=file_id).execute()
    #print file
    print 'Title: %s' % file['title']
    print 'MIME type: %s' % file['mimeType']
    #print 'download_url: %s' file['downloadUrl']
    content = download_file(service, file)
    
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def print_files_in_folder(service, folder_id):
  """Print files belonging to a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  print 'hi'
  page_token = None
  while True:
    try:
      param = {}
      print 'hi'	
      if page_token:
        param['pageToken'] = page_token
      children = service.children().list(
          folderId=folder_id, **param).execute()
      print '################ children ##############33333'
      #print children
      print '################ item ##############33333' 
      item = children.get('items')
      #print item
      for child in children.get('items'):
        print '######## In for loop 333333'
        #content = download_file(service, child)
        #print 'Title: %s' % child['Title']
        print 'File Id: %s' % child['id']
        print_file(service, child['id'])
        #print 'File Name: %s' % child['name']
      page_token = children.get('nextPageToken')
      print page_token
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break

def retrieve_all_files(service):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  print 'In retrive'
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      files = service.files().list(**param).execute()
      print 'hello'
      print files 
      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result

service = createDriveService()
print '################service##################'
#print service
#files = retrieve_all_files(service)
#print '################files##################'
#print files
folder_id = '0BwJnJsT6yrkmY3dhUU5fV1VxaEU'
print_files_in_folder(service, folder_id)
#print_file(service, folder_id)
