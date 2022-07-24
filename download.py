import os 
from Google import Create_Service
import pandas as pd
import requests
import random

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 150)
pd.set_option('display.max_colwidth', 150)
pd.set_option('display.width', 150)
pd.set_option('expand_frame_repr', True)

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'photoslibrary'
API_VERSION = 'v1'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

myAlbums = service.albums().list().execute()
myAlbums_list = myAlbums.get('albums')
dfAlbums = pd.DataFrame(myAlbums_list)
travel_album_id = dfAlbums[dfAlbums['title'] == 'Best Photos for make benefit good slideshow display on the Google Hub']['id'].to_string(index=False).strip()

def download_file(url:str, destination_folder:str, file_name:str):
  response = requests.get(url)
  if response.status_code == 200:
    print('Downloading file{0}'.format(file_name))

media_files = service.mediaItems().search(body={'albumId': travel_album_id}).execute()['mediaItems']

destination_folder = r'~/tmp/testing'

nextPageToken = 'one'

photosRequest = service.mediaItems().search(body={'albumId': travel_album_id})

allPhotos = []

while photosRequest is not None:
    photosResponse = photosRequest.execute()
    photos = photosResponse['mediaItems']
    print('photos list {0}'.format(photos))
    onlyImages = [p for p in photos if p['mimeType']== 'image/jpeg' ]
    print('Only Images {0}'.format(len(onlyImages)))
    print('Photos {0}'.format(len(photos)))
    allPhotos = allPhotos + photos
    photosRequest = service.mediaItems().list_next(photosRequest,photosResponse)

photosForToday = random.sample(range(0, photosResponse - 1), 20)

for index in photosForToday:
    print('Printing index: {0}'.format(index))
    media_file = media_files[index]
    file_name = media_file['filename']
    download_url = media_file['baseUrl'] + '=d'
    download_file(download_url, destination_folder, file_name)

