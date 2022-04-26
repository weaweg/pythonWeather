import requests


class WeatherData:
    __params__ = None

    @staticmethod
    def getUrl():
        return "https://api.openweathermap.org/data/2.5"

    @staticmethod
    def getAppId():
        return "0287af4e2425989d565557e1685cecaa"

    @staticmethod
    def getLang():
        return "pl"

    @staticmethod
    def getCitiesLocations(city, country=""):
        if country != "":
            city += "," + country
        response = requests.get(url="https://api.openweathermap.org/geo/1.0/direct",
                                params=(("q", city), ("limit", 5), ("appid", WeatherData.getAppId())))
        try:
            response.json()[0]
        except (KeyError, IndexError):
            return None
        return list({"name": res["name"],
                     "state": res["state"],
                     "country": res["country"],
                     "lat": res["lat"],
                     "lon": res["lon"]} for res in response.json())

    def setCity(self, lat, lon):
        self.__params__ = [("lat", lat), ("lon", lon),
                           ("appid", self.getAppId()),
                           ("lang", self.getLang())]

    def getCurrentWeather(self):
        return self.__getData__("/weather")

    def getForecastWeather(self):
        return self.__getData__("/forecast")

    def getHistoricalData(self, date):
        return self.__getData__("/onecall/timemachine", date)

    def __getData__(self, endpoint, time=None):
        if self.__params__ is None:
            return None
        self.__params__.append(("dt", time))
        response = requests.get(url=self.getUrl() + endpoint, params=self.__params__)
        if response.status_code != 200:
            return None
        return response.json()
