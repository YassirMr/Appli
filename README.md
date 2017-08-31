# Application
In the context of my internship I was asked to characterize the anechoic chamber R2lab. So after writing some scripts that draw heatmaps of the room in the sense of the received power strength I decided to represent my work in a graphic way and make an analysis tool for the chamber at the same occasion. This application allow you to upload RSSI files that are outcome of some given scripts that can be found here: https://github.com/YassirMr/Internship Then it allows you to draw heatmaps aswell as daily changes in the RSSI between nodes. You can also perform a model fit of the transmission inside the lab.
 This web application has been written in Django. In order to run it you need:
* To have the python3 environment installed 
* Install Django. It can be done using pip as following: 
```
pip install django
```
* Install some dependency libraries. It can be done using pip: 
```
pip install plotly scipy sklearn
```
