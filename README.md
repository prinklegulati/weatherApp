# weatherApp
This App made in Kivy using Python , Searches the weather condition of city . The first screen by defaults take the current location and find weather for current location.Kivy is an open source framework for making GUI apps in python. The main feature of kivy is that the apps builts using Kivy framework are platform independent. Therefore, Apps can be run on desktop , android , ios and on any othe platforms if dependencies installed.


The app uses API of IPstack to determine the current location of the user. An other file has been made in the project that has been imported into main.py to get current location.


To deteremine the weather condition of place this app uses Two APIs of Openweathermap. One as currentweatherdata and other as geocoding API. Although the weather condition can be predicted using only one API viz currentweatherdata But API documentation says that this is not the accurate version to get weather directly by passing city name as parameters and instead parameters must be geolocation cordinates. Also if using directly City name as parameters we can get only one city with taht name. However it is possible to have different cities with Same name. For e.g. London is city in UK as well as in Canada. Therefore Geocoding API first detremines the geo co-ordinates and then passes it to currentweatherdata.
By default if searching nothing this app display the weather of current location 
