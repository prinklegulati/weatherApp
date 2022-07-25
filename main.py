import requests
# importing requests to call API
import sys
#importing sys module to control python runtime environment
from kivy.app import App
#importing App class to run our application
from kivy.properties import StringProperty,NumericProperty
#importing kivy properties
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
# importing different widgets

from getcityname import GetCityName
# importing GetCityName class in order to get current location
# this file is named as getcityname in same project


class WeatherProjApp(App):
    def build(self):
        weatherclass = WeatherClass()
        return weatherclass


class WeatherClass(FloatLayout):
    # This class is the root class and inherits FloatLayout
    # This app calls geocoder API for getting the location attributes of the city searched first
    # and then after getting correct logitude and latitude its call weather API for getting the data
    # However, it is possible to send the name(City Searched) directly to weather API
    # But as per Current Weather Data API documentation this version is less accurate and will be deprecated soon
    # and therefore has been advised to use Geocoder API
    # also , if using directly weatherAPI , it is not possible to get all the cities in world with same name
    # So for Example, there could be more than one city named as London in World such as one in England and one in Canada
    #This is what their documentation reveals:
    #You can use the geocoder built into this API by default,
    #but please note that this version is less accurate than the Geocoder API and will be deprecated soon.
    APIid = ""
    # Here you will need to use your access key for API
    # Access key is same for CurrentWeatherData Api as well as Geocoder API
    # As both API are from openweathermap
    units = "metric"
    # Weather can be taken in any measurement system, I chose Units as metrics system
    # Howevenr Data is aveailable in Metric , Fahrenheit as well as imperical system
    condition_descriptors = StringProperty(None)
    condition_icon = StringProperty(None)
    temperature_description = StringProperty(None)
    maximum_temperature= NumericProperty(None)
    minimum_temperature=NumericProperty(None)
    humidity=NumericProperty(None)
    pressure=NumericProperty(None)
    wind=NumericProperty(None)
    visibility=NumericProperty(None)
    feels_like=NumericProperty(None)
    # Above variable have been made kivy properties in order to use them in .kv file
    getcurrentloc=GetCityName()
    getcurrentinfo=getcurrentloc.getcurrentlocattributes()
    #getcurrentinfo has been made variable to hold the current location data
    #getcurrentinfo will be invalid in case of no internet connectivity
    #as specified in getcityname file
    if(getcurrentinfo=="invalid"):
        sys.exit("Internet is not available")
    # Therefore, in case of no internet connectivity system will exit and will not run application
    current_city=getcurrentinfo['city']
    current_longitude=getcurrentinfo['longitude']
    current_latitude=getcurrentinfo['latitude']
    """The ipstack API as called in getcityname files provides geo coordinates as well ,
    therefore for the current location of user we don't need to call geocoder API
    and current weather data api can be called directly"""
    parameters = {
        "lat": current_latitude,
        "lon": current_longitude,
        "appid": APIid,
        "units": units
    }
    dropdown = DropDown(size_hint=(1, .1),
                        pos_hint={'right': 1, 'top': 0.9})
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation="horizontal"
        textinput = TextInput(text=self.current_city, size_hint=(.7, .1),
                              pos_hint={'right': 0.7, 'top': 1})
        button = Button(text="Search",
                        size_hint=(.3, .1),
                        pos_hint={'right': 1, 'top': 1})
        button.bind(on_press=lambda button: self.buttonFunction(textinput.text))
        #buttonfunction method has been binded with this button on press event
        # this function basically takes the input of user which is city name to be searched for
        # and create the dropdown for different places in world with same name
        mainbutton = Button(text=str(textinput.text), size_hint=(1, .1),
                            pos_hint={'right': 1, 'top': 0.9})
        # We are not adding any dropdown for current location as current location can't be more than one
        # therefore instead of creating dropdown here a button with same name as current location has been created
        # this has been exclusively define in constructor so that our first screen can show weather of current location
        self.add_widget(textinput)
        self.add_widget(button)
        self.add_widget(mainbutton)
        self.dropfunction(self.parameters,self.dropdown,mainbutton)
        """ drop function takes the specific locations founded by buttonfunction and then resets the current 
        variables correspondingly to be shown in app and these variables then can be accessed in .ky file"""

    def gettcitiesLongandLot(self, text):
        """ This is the function that is used to get longitude and latitude
        of the city searched for , Note here that this function fetches the long
        and lat of all the cities with same name . Basically this is the function
        which helps us to know the different geographical cities with same name with their geo coordinates"""
        baseURL="http://api.openweathermap.org"
        endpoints="/geo/1.0/direct"
        URL=baseURL+endpoints
        param={
            'q': text,
            'limit':'5',
            'appid':'b62cb3f2a3cc1514e250f0c76b4007dc'
        }
        try:
            response = requests.get(URL,params=param)
            names = response.json()
            # print(names)
            return names
        except requests.exceptions.ConnectionError as e:
            print("Connection cant be established")
            sys.exit("no internet connectivity")
            # although connection connectivity was checked before as well in getcityname file
            # and application won't start in case of no network connectivity
            # but it is possible that some user was connected to internet at any time when application was started
            # But application was not closed and now when city is being searched , user is not connected to internet anymore
        except requests.exceptions.JSONDecodeError as e:
            print("Make sure API call is correct, There seems to be problem with API addess")
            # if anyhow endpoint goes wrong for example while refracting the code or anyhow
            # json code error exception will be thrown , as otherwise if checking with status code==200
            # this can go wrong as in case of error only in endpoint but in baseURL
            # still response with status code 200 will be received with success=failre in content

    def buttonFunction(self, text):
        names = self.gettcitiesLongandLot(text)
        dropdown = DropDown(size_hint=(1, .1),
                            pos_hint={'right': 1, 'top': 0.9})
        for city in names:
            if "state" not in city:
                city['state'] = city['name']
            btn = Button(text='% s  %s  %s' % (city['name'], city['state'], city['country']), size_hint_y=None,
                         height=40)
            parameters = {
                "lat": city['lat'],
                "lon": city['lon'],
                "appid": self.APIid,
                "units": self.units
            }
            btn.id = parameters
            btn.bind(on_release=lambda btn: self.dropfunction(btn.id, dropdown, btn))
            dropdown.add_widget(btn)
            dropdown.select(btn.text)
            """The above for loop will create buttons for different cities found with same name and will add them ro 
            dropdown menu .However question arises that in case if user enters the name of the city which is 
            inaccurate or in other terms no such city exist in World , Then this loop will not be executed as the 
            response array will contain no value or in other term it will be empty """
        mainbutton = Button(text=self.dropdowntext(names) + str(text), size_hint=(1, .1),
                            pos_hint={'right': 1, 'top': 0.9})
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        self.add_widget(mainbutton)

    def dropdowntext(self,names):
        """This function find what is to be displayed on Drop Down menu for example if no result is found for searched term
         then this will display We couldn't find any result for searched term """
        if len(names)==0:
            text="Sorry, We couldn't find any result for";
        else:
            text="following results have been found for"
        return text


    def dropfunction(self, parameters, dropdown, btn):
        """this function will run when a city from dropdown will be selected as stated before drop function takes the
        specific locations founded by buttonfunction and then resets the current variables correspondingly to be
        shown in app and these variables then can be accessed in .ky file. This function is responsible for setting all
        weather related variables as this function calls currentweatherAPI and receives response """
        dropdown.select(btn.text)
        # print(parameters)
        # for i in self.children:
        #     if type(i) == kivy.uix.label.Label:
        #         self.remove_widget(i)
        try:
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather", params=parameters)
            if(response.status_code==200):
                response = response.json()
        except requests.exceptions.ConnectionError as e:
                print("internet is not available")
                sys.exit("Something went wrong")
            # Internet connectivity is checked here once again because it is again possible that at some
            #user has internet connectivity when searching for city but has lost it now
        self.condition_descriptors = str(response['weather'][0]["main"]) + "," + str(
            response['weather'][0]["description"])
        self.condition_icon = "./images/" + str(response['weather'][0]["icon"]) + ".png"
        self.temperature_description = "Temperature is %d" % (response['main']["temp"])
        self.maximum_temperature=response['main']['temp_max']
        self.minimum_temperature=response['main']['temp_min']
        self.humidity=response['main']['humidity']
        self.visibility=response['visibility']
        self.feels_like=response['main']['feels_like']
        self.wind=response['wind']['speed']
        self.pressure=response['main']['pressure']
        # print(response['main']['temp'])
        # print(response)
        # print("I am called")
        # return response
        # label1 = Label(
        #     text="Temprature is %d and feels like %d" % (response['main']['temp'], response['main']['feels_like']))
        # label = Label(text='%s , %s' % (response['weather'][0]['main'], response['weather'][0]['description']))
        # self.add_widget(label)
        # self.add_widget(label1)


if __name__ == '__main__':
    WeatherProjApp().run()
