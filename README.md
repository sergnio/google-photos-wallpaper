# Work in progress!
## MacOS Setup 
1. Clone this repo\
  a. Install all dependencies using `python -m pip install -r requirements.txt`\
  b. Add a `config.json` (see below for format) in the same directory as the other files in this repo\
  c. Add your destination path as the `value` to the `key` `destinationFolder`\
  d. Add your Google Photos Album name as the `value` to the `key` `albumName`\
     **Note:** The name must be exact!!\
1. Create (or reuse an existing) Google API service account\
  a. As of July 24, 2022, this tutorial has a button that very easily allows you to: https://developers.google.com/photos/library/guides/get-started\
  b. Download the `credentials.json` file and place it in this same directory\
1. Install this to run automatically on your computer\
  a. `cd` to your `/Library/LaunchAgents` directory\
  **Note:** There is also a `/Users/{your-user}/Library/LaunchAgents/` directory. To my understanding, this will only apply this to your user, not to all users on the machine. Also, I'm not totally sure if it works when working out of this directory :)\
  b. Create a `plist` file which will be used by `launchd` to run automatically using: `touch com.gphotos.wallpaper.plist`.\
  You can probably name it whatever you want, but this is what I used.\
  c. `vim` into that file and copy the contents below\
  d. Update your path to be wherever you installed this repo. For me, the path I used was `/Users/sergnio/projects/google-photos-wallpaper`\
  e. Update your path to wherever your python is installed. I used homebrew, so I used the location where homebrew installed it.
  f. FINALLY, let's run a command to properly run this automatically: `sudo launchctl bootstrap gui/501 com.gphotos.wallpaper.plist`
 
Example `config.json`
```
{
 "albumName": "Best Photos for make benefit good slideshow display on the Google Hub",
 "destinationFolder": "/Users/sergnio/Pictures"
}
```

Example `com.gphotos.wallpaper.plist`
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>

    <key>Label</key>
    <string>com.gphotos.wallpaper.plist</string>

    <key>RunAtLoad</key>
    <true/>

    <key>StartInterval</key>
    <integer>86400</integer>

    <key>StandardErrorPath</key>
    <string>YOUR-PATH-HERE/google-photos-wallpaper/stderr.log</string>  <-- replace this with your path where you installed this repo

    <key>StandardOutPath</key>
    <string>YOUR-PATH-HERE/google-photos-wallpaper/stdout.log</string>  <-- replace this with your path where you installed this repo

    <key>WorkingDirectory</key>
    <string>YOUR-PATH-HERE/google-photos-wallpaper</string> <-- replace this with your path where you installed this repo

    <key>ProgramArguments</key>
      <array>
        <string>/opt/homebrew/bin/python3</string> <-- I used homebrew to install python, so point to whichever directory works for you
        <string>YOUR-PATH-HERE/google-photos-wallpaper/download.py</string>
      </array>

  </dict>
</plist>
```

## Troubleshooting
**Change the frequency**\
In your `com.gphotos.wallpaper.plist` file, just change `StartInterval` value to something something else in seconds, and also change your frequency in your desktop & screensavers app on your mac.\
e.g. running it every hour would be **3600** instead of **86400** (60 [seconds] * 60 [minutes] = 3600 [seconds])\

**Stopping the daemon**\
Just run `sudo launchctl bootout gui/501 com.gphotos.wallpaper.plist` instead

**Seeing errors**\
Run a `tail -f stderror.log` to see a live view of your logs, otherwise `vim stderror.log` to see what errors there are.\

**Instructions unclear**\
Feel free to drop an issue on this repo and I'm happy to help out!
