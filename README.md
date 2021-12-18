# retroVideoDownloader
* The target is to download specific media and information of games from a console chosen.
* The <i><b>input</b></i> is a <i><b>console url</i></b> that is saved in the <i><b>config file</i></b>. The process will navigate to that console url and will fetch the desired results for all the games listed under that console.
* To start the process install the requirements and run <b><i>Main.py</i></b>

## Requirements & Installation

* Install Requirements using ``pip install -r requirements.txt``

* It will install these following modules:-

> ```Pandas : Used for data handling (file read-write operations)```

> ```Selenium : Used for automating a chrome browser```

> ```Requests : Used for https request```

> ```Numpy : Comprehensive mathematical functions, random number generators```

> ```Mutagen : To handle meta tags for video```

> ```Moviepy : Module for video editing```


* <b>Gecko Driver </b>
  > Install the geckodriver from https://github.com/mozilla/geckodriver/releases based on your system configuration 
    
    <b> OR</b>
   > Use from the repo and do the following steps.
   
   > ```cp geckodriver /usr/local/bin```

  > ```chmod +x /usr/local/bin/geckodriver```
  
  > ```chmod +x geckodriver``` 
    
    <b> OR</b>
  
  > ```wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz```
  
  > ```tar -xf geckodriver-v0.29.1-linux64.tar.gz```
  
  > ```rm geckodriver-v0.29.1-linux64.tar.gz```
  
  > ```cp geckodriver /usr/local/bin```

  > ```chmod +x /usr/local/bin/geckodriver```
  
  > ```chmod +x geckodriver```

  >Add SUDO if permission denied

* <b>Mozilla Firefox </b>
  > Install the latest firefox on your system from the link  https://www.mozilla.org/en-US/firefox/new/ .
  
  <b> OR</b>

   > ```sudo apt install firefox```
  

## CONFIG

*  <b>GECKO_DRIVER_PATH:</b> The path where gecko driver is located.

*  <b>HEADLESS_BROWSER:</b> Option to run process in browser mode or in headless mode.

*  <b>FILE_NAME_SEPARATOR:</b> String that will be used to separate assets file name convention.

*  <b>REMOVE_SECONDS_VIDEO:</b> Float value. It can be 0.6 for example. The duration which will be trimmed in videos.

*  <b>DATABASE_FILE_PATH:</b> FilePath for the database file.

*  <b>SKIP_DATABASE_FILE:</b> Option to skip database file if needed.

*  <b>FOLDER_TO_SAVE:</b> Folder where the assets and video will be downloaded.

*  <b>POST_PROCESSING_OVERLAY_ENABLE:</b> Option to do post processing overlay on videos or not.

*  <b>OVERLAY_FILE_ORDER:</b> Option to chose overlay file from this comma separated values (Wheel,3D_Box,3D_Support). Overlay file will be chosen on the basis of availability of high priority media for a game.

*  <b>CONSOLE_URL:</b> console type for downloading the media of games.
