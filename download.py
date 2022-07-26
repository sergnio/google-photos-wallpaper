import os
from Google import Create_Service
import pandas as pd
import requests
import random
import json
import time
import datetime

# override the gioPrint so it prints to a file instead
def gioPrint(toPrint:str):
    print('{0}: {1}'.format(datetime.datetime.now(),toPrint))

config = None
gioPrint('Reading config file')
configLocation = 'config.json'
# JSON file
with open (configLocation, "r") as f:
    config = json.loads(f.read()) 
    f.close()
albumName = config['albumName']
destination_folder = config['destinationFolder']
gioPrint('Config successfully loaded')

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
    gioPrint('Downloading file{0}'.format(file_name))
    with open(os.path.join(destination_folder, file_name), 'wb') as f:
            f.write(response.content)
            f.close()

nextPageToken = 'one'

photosRequest = service.mediaItems().search(body={'albumId': travel_album_id})

allPhotos = []

start = time.time()
while photosRequest is not None:
    photosResponse = photosRequest.execute()
    photos = photosResponse['mediaItems']
    onlyImages = [p for p in photos if p['mimeType']== 'image/jpeg' ]
    gioPrint('Adding {0} images to array'.format(len(onlyImages)))
    allPhotos = allPhotos + onlyImages 
    photosRequest = service.mediaItems().list_next(photosRequest,photosResponse)

end = time.time()
gioPrint('Requests took {0} seconds'.format(round(end-start),2))
writeToFile = destination_folder + '/allPhotos.json'

# creates directory if it doesn't exist
os.makedirs(destination_folder, exist_ok=True) 

gioPrint('Writing payload to file: {0}'.format(writeToFile))
with open(writeToFile, 'w+') as f:
    json.dump(allPhotos, f)
    f.close()

photosForToday = random.sample(range(0, len(allPhotos) - 1), 20)
gioPrint('Number of Photos available {0}'.format(len(allPhotos)))

for index in photosForToday:
    gioPrint('Printing index: {0}'.format(index))
    media_file = allPhotos[index]
    file_name = media_file['filename']
    download_url = media_file['baseUrl'] + '=d'
    download_file(download_url, destination_folder, file_name)

