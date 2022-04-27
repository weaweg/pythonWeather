import requests


class WeatherApi:
    def __init__(self):
        self.__params = {"appid": self.getAppId(),
                         "lang": "pl",
                         "units": "metric"}

    @staticmethod
    def getAppId():
        f = open("api_code.txt", "r")
        return f.read()

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
                if (city["name"], city["state"]) not in [(c["name"], c["state"]) for c in cities]:
                    cities.append(city)

            return cities
        except (KeyError, IndexError, TypeError):
            return None

    def setLocation(self, lat, lon):
        self.__params["lat"] = lat
        self.__params["lon"] = lon


    def getForecastWeather(self):
        params = {"exclude": "current,minutely,daily,alerts"}
        return self.__getData(params, "/onecall")

    def getHistoricalData(self, dt):
        params = {"dt": dt}
        return self.__getData(params, "/onecall/timemachine")

    def __getData(self, params=None, endpoint=""):
        if self.__params is None:
            return None
        if params is not None:
            params = self.__params | params
        response = requests.get(url="https://api.openweathermap.org/data/2.5" + endpoint, params=params)
        if response.status_code != 200:
            return None
        return response.json()
