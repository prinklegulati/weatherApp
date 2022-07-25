import requests
# importing requests to call API



class GetCityName:
    """ This class class API IPStack in order to get the current location of user
    Our Application first screen display the weather conditions for current location"""

    def __init__(self):
        self.parameters={
            "access_key":""
        }
        self.baseurl="http://api.ipstack.com/check"

    def getcurrentlocattributes(self):
        try:
            response=requests.get(self.baseurl,params=self.parameters)
            if(response.status_code==200):
                response=response.json()
        except requests.exceptions.ConnectionError as e:
            print("Something Went Wrong")
            response="invalid"
        finally:
            # print(response)
            return response