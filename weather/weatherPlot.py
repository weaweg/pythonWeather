from datetime import datetime

from matplotlib.figure import Figure
import matplotlib.patches as mpatches


class WeatherPlot(Figure):

    def __init__(self):
        super().__init__(figsize=(12, 8), dpi=90, layout="constrained")

    def forecastPlot(self, data, city, state, country):
        processed = {"time": [], "temp": [], "pressure": [], "clouds": [], "humidity": []}
        for point in data["list"]:
            date = datetime.fromtimestamp(point["dt"])
            processed["time"].append(date)
            processed["temp"].append(point["main"]["temp"])
            processed["pressure"].append(point["main"]["pressure"])
            processed["clouds"].append(point["clouds"]["all"])
            processed["humidity"].append(point["main"]["humidity"])
        self.__weatherPlot(processed, city, state, country, "Prognoza", 0)

    def historicalPlot(self, data, city, state, country):
        processed = {"time": [], "temp": [], "pressure": [], "rain": [], "humidity": []}
        for point in data["hourly"]:
            date = datetime.fromtimestamp(point["dt"])
            processed["time"].append(date.strftime("%H:%M"))
            processed["temp"].append(point["temp"])
            processed["pressure"].append(point["pressure"])
            processed["clouds"].append(point["clouds"])
            processed["humidity"].append(point["humidity"])
        day = datetime.fromtimestamp(data["hourly"][0]["dt"]).strftime("%d.%m.%y")
        self.__weatherPlot(processed, city, state, country, day, 45)

    def __weatherPlot(self, processed, city, state, country, day, rot):
        self.__addPlot(processed["time"], processed["temp"], processed["pressure"], city, state, country, day, rot, 211)
        self.__addPlot(processed["time"], processed["clouds"], processed["humidity"], city, state, country, day, rot, 212)

    def __addPlot(self, x, y, z, city, state, country, day, rot, pos):
        a = self.add_subplot(pos)
        a.minorticks_on()
        a.tick_params(axis='x', labelrotation=rot)
        a.set_title(f"{day}: pogoda dla {city} - {state} - {country}")
        a.set_ylabel(u"Temperatura (\u00B0C)")
        a.plot(x, y, "r-")

        b = a.twinx()
        b.minorticks_on()
        b.set_ylabel("Ciśnienie (hPa)")
        b.plot(x, z, "b-")

        temp = mpatches.Patch(color='red', label='Temperatura')
        press = mpatches.Patch(color='blue', label='Ciśnienie')
        a.legend(handles=[temp, press], loc="upper right", framealpha=1)