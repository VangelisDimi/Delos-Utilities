![alt text](https://github.com/VangelisDimi/Delos-Utilities/blob/master/Assets/uoa_logo_128.png?raw=true)
# Delos Utilities
A simple tool that lets you create VLC playlists from Delos resources and helps with downloading them.


# Use 
You enter links which can be either from a video like [this one](https://delos.uoa.gr/opendelos/videolecture/show?rid=d4da42eb) or from a search result like [this one](https://delos.uoa.gr/opendelos/search?crs=7c964daa-86c08dd4&vy=2020&st=fc977aae) and you can either create a VLC .xspf playlist or get the responding file links to use in a video downloader app like [this one](https://github.com/MrS0m30n3/youtube-dl-gui/releases). The link types can be combined.   
When you select to include all search pages,all the following search pages after the ones you inserted will be included.  
When you enter a search page you can choose which specific videos you want to include.  
You can also rename downloaded videos to give them the correct resource name (the files have names like 112fhfkf.mp4).


# How to Run
Install dependecies
```
pip3 install -r requirments.txt
```
Run
```
python3 gui.py
```

# Licenses
## Icons
https://www.iconfinder.com/iconsets/google-material-design-icons  
https://creativecommons.org/licenses/by-sa/3.0

## Code
https://github.com/cnasikas/delos-downloader  
MIT License