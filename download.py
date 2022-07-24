import os 
from Google import Create_Service
import pandas as pd
import requests
import random
import json
import time

albumName = input('What is your album name? (the name must exactly match):')

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
travel_album_id = dfAlbums[dfAlbums['title'] == albumName]['id'].to_string(index=False).strip()

def download_file(url:str, destination_folder:str, file_name:str):
  response = requests.get(url)
  if response.status_code == 200:
    print('Downloading file{0}'.format(file_name))
    with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)
            f.close()

destination_folder = r'/tmp/testing'
nextPageToken = 'one'

photosRequest = service.mediaItems().search(body={'albumId': travel_album_id})

allPhotos = []

start = time.time()
while photosRequest is not None:
    photosResponse = photosRequest.execute()
    photos = photosResponse['mediaItems']
    onlyImages = [p for p in photos if p['mimeType']== 'image/jpeg' ]
    print('Adding {0} images to array'.format(len(onlyImages)))
    allPhotos = allPhotos + onlyImages 
    photosRequest = service.mediaItems().list_next(photosRequest,photosResponse)

end = time.time()
print('Requests took {0} seconds'.format(round(end-start),2))
writeToFile = r'/tmp/testing/allPhotos.json'
print('Writing payload to file: {0}'.format(writeToFile))
with open(writeToFile, 'w+') as f:
    json.dump(allPhotos, f)

photosForToday = random.sample(range(0, len(allPhotos) - 1), 20)
print('Number of Photos available {0}'.format(len(allPhotos)))

for index in photosForToday:
    print('Printing index: {0}'.format(index))
    media_file = allPhotos[index]
    file_name = media_file['filename']
    download_url = media_file['baseUrl'] + '=d'
    download_file(download_url, destination_folder, file_name)

