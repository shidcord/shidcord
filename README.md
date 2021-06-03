# shidcord
A few modifications to the Discord Web Client, like invisible self-hosted/encrypted DMs/group chats/servers

### WARNING!!! THIS PROGRAM IS IN EARLY ALPHA! USE AT YOUR OWN RISK

## Introductions
Shidcord is essentially modifications to the web client, and requires a lot of work to set up as of now.
It is in very early stages of development, so join the [discord](https://discord.gg/YZW6tZBJ2k) for additional help or to help speed the development of this software.
**Notice: Google Chrome, or a chromium browser with support for Chrome extensions, is recommended. All other browsers are YMMV.**


## Browser Setup
To get started, install the [TamperMonkey](https://www.tampermonkey.net) extension, as well as [Allow CORS](https://chrome.google.com/webstore/detail/allow-cors-access-control/lhobafahddgcelffkeicbaginigeejlf) and [Always Disable CSP](https://chrome.google.com/webstore/detail/always-disable-content-se/ffelghdomoehpceihalcnbmnodohkibj). These extensions are required to allow the script software to run.
Go to TamperMonkey, create a new script, and paste the following code:
`// ==UserScript==
// @name         Discord api redirect
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        *://*/*
// @include      http://discord.com/api/v9/channels/<CHANNEL ID>*
// @include      *//localhost:8000/api/v9/channels/<CHANNEL ID>*
// @grant        GM_webRequest
// ==/UserScript==

//CHANGE "<CHANNEL ID>" to the channel ID of the group chat you want to intercept api calls for

var currently_active_webrequest_rule = JSON.stringify(GM_info.script.webRequest); // == @webRequst header from above

GM_webRequest([
    //{ selector: '*cancel.me/*', action: 'cancel' },
    //{ selector: { include: '*', exclude: 'http://exclude.me/*' }, action: { redirect: 'http://localhost:8000/api' } },
    { selector: { match: '*://discord.com/api/v9/channels/<CHANNEL ID>/*' }, action: { redirect: { from: 'https://discord.com/api/v9/channels/<CHANNEL ID>/(.*)',  to: 'http://localhost:8000/api/v9/channels/<CHANNEL ID>/$1' } } }
], function(info, message, details) {
    console.log(info, message, details);
});`
Alpha-3 note: you will have to change the <channel id> to the dev id of the chat you will intercept. Go to Discord, and enable developer mode. Then right-click on a channel(a private server where no one has joined is preferred), and select copy ID. Paste the ID into the places that say <Channel ID>, and make sure to fully replace that text with the ID.
  
Next, you set up the server to allow api calls from localhost.

On chrome and equivalent:
  Click Ctrl+Shift+I on discord.com
  Click on the dropdown to reveal more tabs
  Click on Application
  Click on Local Storage, then discord.com
  Find gatewayUrl, then double-click the text that says, "wss://gateway.discord.gg"
  Replace it with "ws://127.0.0.1"
  You are ready for Setup: Part 2
On firefox and equivalent:
  Click Ctrl+Shift+I
  Click on Storage(via dropdown or such)
  Click on Local Storage, then discord.com
  Find gatewayUrl, then double-click the text that says, "wss://gateway.discord.gg"
  Replace it with "ws://127.0.0.1"
  You are ready for Setup: Part 2

## Websockets Setup
Windows: ** WARNING: THE WEBSOCKET LIBRARY CURRENTLY DOES NOT WORK ON WINDOWS, A FIX WILL SOON COME. As a result, the autosockets script has not been developed for alpha-3 yet, but for the purpose of theory, the steps to get it running are down below.**
  Download the main branch of this repo, then extract the zip. Make sure you have pip3 installed, then open cmd and type: `pip3 install simple-websocket-server websocket-client` You will have all required files in order to start your server. 
  **notice: you will have to follow the steps below every time**
  Open cmd in the current directory, and type `set FLASK_APP=flask_server.py`. Run it, then run `python3 -m flask run --host=localhost --port=8000`. This will set up your flask server.
  Open up a new cmd window, and type `python3 wsServer.py`. It should stay empty, until you visit discord.com, where you will see data being sent around.
Linux: There are two options. Autosockets.py, or the manual method, which differs from the Windows Manual Method.
  **Autosockets**:
    Download the latest `autosockets.py` from the releases page, and place it in its separate directory. **Make sure you have `wget` installed**
    Next, run `sudo python3 autosockets.py`. Because this relies on websockets, Linux requires root to allow this port to be passed through. You should see a bunch of files being downloaded, dependencies being installed(**Make sure you have pip3 installed!**), and it ending with how to kill the server. You should be able to open discord.com, and connect. Nothing will appear yet, as this is still in alpha, but it means you have successfully got Shidcord to run on your device!
   **Manual**:
    Download the main branch of this repo, then extract the zip. Make sure you have pip3 installed, then open cmd and type: `sudo pip3 install simple-websocket-server websocket-client` You will have all required files in order to start your server. 
  **notice: you will have to follow the steps below every time**
  Open terminal in the current directory, and type `export FLASK_APP=flask_server.py`. Run it, then run `python3 -m flask run --host=localhost --port=8000`. This will set up your flask server.
  Open up a new terminal, and type `sudo python3 wsServer.py`. It should stay empty, until you visit discord.com, where you will see data being sent around. Nothing new will appear on discord, as this is still in alpha, but it means you have successfully got Shidcord to run on your device!
  
  
## Disclaimers and Bugs
  All dependencies for this program: python3, pip3, wget(for linux), a browser based on Chrome or Firefox, sudo(for linux)
  This still needs an encryption algorithim, that is being worked on.
  The real functionality of this program is still being worked on. If you are a brave soul, the program is up to uncomment and change values.
  If you would like to support development, JOIN THE [DISCORD SERVER](https://discord.gg/YZW6tZBJ2k)
