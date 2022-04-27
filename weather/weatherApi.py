import requests


class WeatherApi:
    def __init__(self):
        self.__params = None

    @staticmethod
    def getUrl():
        return "https://api.openweathermap.org/data/2.5"

    @staticmethod
    def getAppId():
        f = open("api_code.txt", "r")
        return f.read()

    @staticmethod
    def getLang():
        return "pl"

    @staticmethod
    def getCityLocation(city, country):
        if city is None or city == "":
            return None
        city += "," + country
        response = requests.get(url="https://api.openweathermap.org/geo/1.0/direct",
                                params=(("q", city), ("limit", 5), ("appid", WeatherApi.getAppId())))
        try:
            cities = []
            for res in response.json():
                city = {"name": res["name"],
                        "state": res["state"],
                        "country": res["country"],
                        "lat": res["lat"],
                        "lon": res["lon"]}
                if "local_names" in res:
                    if "pl" in res["local_names"]:
                        city["name"] = res["local_names"]["pl"]
                cities.append(city)
            return cities
        except (KeyError, IndexError, TypeError):
            return None

    def setCity(self, lat, lon):
        self.__params = {"lat": lat, "lon": lon,
                           "appid": self.getAppId(),
                           "lang": self.getLang(),
                           "units": "metric"}

    def getCurrentWeather(self):
        return self.__getData("/weather")

    def getForecastWeather(self):
        return self.__getData("/forecast")

    def getHistoricalData(self, dt):
        return self.__getData("/onecall/timemachine", dt)

    def __getData(self, endpoint, dt=0):
        if self.__params is None:
            return None
        self.__params["dt"] = dt
        response = requests.get(url=self.getUrl() + endpoint, params=self.__params)
        if response.status_code != 200:
            return None
        return response.json()
