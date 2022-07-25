# Work in progress!
## Setup
1. Clone this repo
  a. Install all dependencies using `python -m pip install -r requirements.txt`
1. Create (or reuse an existing) Google API service account
  a. As of July 24, 2022, this tutorial has a button that very easily allows you to: https://developers.google.com/photos/library/guides/get-started
  b. Download the `credentials.json` file and place it in this same directory
11. Install cron job\
  a. crontab -e
  b. 

// needs this permission
sudo chmod 600 com.buddy.background.plist
// nice command to check if it's a valid plist
plutil -lint filename
