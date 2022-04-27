from datetime import datetime

import matplotlib.patches as patches
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure


class WeatherPlot(Figure):

    def __init__(self):
        super().__init__(figsize=(12, 8), dpi=90)
        self.__paramsPlot = [[u"Temperatura [\u00B0C]", "Ciśnienie [hPa]", "red", "blue"],
                             ["Zachmurzenie [%]", "Wilgotność [%]", "grey", "orange"]]
        self.__city = None
        self.__state = None
        self.__country = None
        self.__rot = 0

    def forecastPlot(self, data, city, state, country):
        self.__city = city
        self.__state = state
        self.__country = country
        processed = {"time": [], "temp": [], "pressure": [], "clouds": [], "humidity": []}
        for point in data["hourly"]:
            date = datetime.fromtimestamp(point["dt"])
            processed["time"].append(date)
            processed["temp"].append(point["temp"])
            processed["pressure"].append(point["pressure"])
            processed["clouds"].append(point["clouds"])
            processed["humidity"].append(point["humidity"])
        self.__weatherPlot(processed, "Prognoza", "%H:%M\n%d.%m")

    def historicalPlot(self, data, city, state, country):
        self.__city = city
        self.__state = state
        self.__country = country
        processed = {"time": [], "temp": [], "pressure": [], "clouds": [], "humidity": []}
        for point in data["hourly"]:
            date = datetime.fromtimestamp(point["dt"])
            processed["time"].append(date.strftime("%H:%M"))
            processed["temp"].append(point["temp"])
            processed["pressure"].append(point["pressure"])
            processed["clouds"].append(point["clouds"])
            processed["humidity"].append(point["humidity"])
        text = datetime.fromtimestamp(data["hourly"][0]["dt"]).strftime("%d.%m.%y")
        self.__rot = 45
        self.__weatherPlot(processed, text, None)

    def __weatherPlot(self, processed, text, dateformat):
        self.__addPlot(processed["time"], processed["temp"], processed["pressure"], text, 211, 0, dateformat)
        self.__addPlot(processed["time"], processed["clouds"], processed["humidity"], text, 212, 1, dateformat)

    def __addPlot(self, x, y, z, text, pos, i, dateFormat):
        a = self.add_subplot(pos)
        a.minorticks_on()
        a.tick_params(axis='x', labelrotation=self.__rot)
        if pos == 211:
            a.set_title(f"{text}: pogoda dla {self.__city} - {self.__state} - {self.__country}")
        a.set_ylabel(self.__paramsPlot[i][0])
        a.plot(x, y, self.__paramsPlot[i][2])
        if dateFormat is not None:
            a.xaxis.set_major_formatter(DateFormatter(dateFormat))

        b = a.twinx()
        b.minorticks_on()
        b.set_ylabel(self.__paramsPlot[i][1])
        b.plot(x, z, self.__paramsPlot[i][3])

        paramLeg1 = patches.Patch(color=self.__paramsPlot[i][2], label=self.__paramsPlot[i][0])
        paramLeg2 = patches.Patch(color=self.__paramsPlot[i][3], label=self.__paramsPlot[i][1])
        b.legend(handles=[paramLeg1, paramLeg2], loc="upper right", framealpha=1)
