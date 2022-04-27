import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
from datetime import datetime

from weather import WeatherApi
from weather import WeatherPlot

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class WeatherGUI:
    __pd__ = "15 5"

    def __init__(self):
        self.__root = tk.Tk()
        self.__root.resizable(False, False)
        self.__root.eval("tk::PlaceWindow . center")
        self.__root.title("WeatherApp 2022 by BudzowskiB")
        self.__weatherApi = WeatherApi()
        self.__cityInput = tk.StringVar()
        self.__countryInput = tk.StringVar()

    def start(self):
        self.__initGUI()

    def exit(self):
        self.__root.destroy()

    def __initGUI(self):
        self.__optionFrame = ttk.Frame(self.__root, padding=self.__pd__)
        self.__optionFrame.grid()
        self.__optionFrame.grid_remove()
        ttk.Button(self.__optionFrame, text="Prognoza pogody", command=self.__showForecast).grid(columnspan=2, row=0)
        self.__dateBox = ttk.Combobox(self.__optionFrame, state="readonly",
                                      values=["Wczoraj", "Przedwczoraj", "Trzy dni temu", "Cztery dni temu",
                                              "Pięć dni temu"])
        self.__dateBox.current(0)
        self.__dateBox.grid(column=0, row=1)
        ttk.Button(self.__optionFrame, text="Wyświetl", command=self.__showHistorical).grid(column=1, row=1)

        searchFrame = ttk.Frame(self.__root, padding=self.__pd__)
        searchFrame.grid(column=1, row=0)

        ttk.Label(searchFrame, text="Miasto").grid(column=0, row=0)
        cityEntry = ttk.Entry(searchFrame, textvariable=self.__cityInput)
        cityEntry.grid(column=0, row=1)

        ttk.Label(searchFrame, text="Kod państwa").grid(column=1, row=0)
        countryEntry = ttk.Entry(searchFrame, textvariable=self.__countryInput)
        countryEntry.grid(column=1, row=1)

        ttk.Button(searchFrame, text="Szukaj", command=self.__getCityLocation).grid(column=2, row=1)

        self.__dataFrame = ttk.Frame(self.__root, padding=self.__pd__)
        self.__dataFrame.grid(column=0, columnspan=2, row=1)
        dataLabel = ttk.Label(self.__dataFrame, text="Wybierz miasto aby wyświetlić pogodę")
        dataLabel.pack()

        tk.mainloop()

    def __getCityLocation(self):
        cities = WeatherApi.getCityLocation(self.__cityInput.get(), self.__countryInput.get())
        if cities is None or len(cities) == 0:
            msgbox.showinfo("Informacja", "Nie znaleziono miasta")
            return
        pickCity = tk.Toplevel()

        pickCity.title("Wybierz miasto")
        pickCity.resizable(False, False)
        pickCity.grab_set()
        cityTreeView = ttk.Treeview(pickCity, height=5, show="headings", selectmode="browse")
        cityTreeView["columns"] = ("LP", "Name", "State", "Country", "Lat", "Lon")
        for column in cityTreeView["columns"]:
            cityTreeView.column(column, minwidth=30, width=100, anchor=tk.CENTER)
            cityTreeView.heading(column, text=column)
        cityTreeView.column("LP", width=30)
        for i in range(len(cities)):
            city = list(cities[i].values())
            city.insert(0, i + 1)
            cityTreeView.insert("", tk.END, values=city)
        cityTreeView.grid(column=1, columnspan=3, row=1)
        ttk.Button(pickCity, text="Wybierz",
                   command=lambda: self.__setCity(pickCity, cityTreeView, cities)).grid(column=2, row=2)
        self.center(pickCity)

    def __setCity(self, pickCity, cityTreeView, cities):
        index = cityTreeView.index(cityTreeView.focus())
        self.__weatherApi.setCity(cities[index]["lat"], cities[index]["lon"])
        self.__city = cities[index]["name"]
        self.__state = cities[index]['state']
        self.__country = cities[index]["country"]
        pickCity.destroy()
        self.__showForecast()

    def __showForecast(self):
        forecastData = self.__weatherApi.getForecastWeather()
        if forecastData is None:
            msgbox.showerror("Błąd", "Błąd pobierania danych")
            return
        fig = WeatherPlot()
        fig.forecastPlot(forecastData, self.__city, self.__state, self.__country)
        self.__drawPlot(fig)

    def __showHistorical(self):
        time = datetime.timestamp(datetime.now()).__trunc__()
        pos = self.__dateBox.current() + 1
        historicalData = self.__weatherApi.getHistoricalData(time - pos * 86400)
        if historicalData is None:
            msgbox.showerror("Błąd", "Błąd pobierania danych")
            return
        fig = WeatherPlot()
        fig.historicalPlot(historicalData, self.__city, self.__state, self.__country)
        self.__drawPlot(fig)

    def __drawPlot(self, fig):
        try:
            self.__dataFrame.winfo_children()[0].destroy()
        except IndexError:
            pass
        canvas = FigureCanvasTkAgg(fig, master=self.__dataFrame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.__optionFrame.grid()
        self.center(self.__root)

    @staticmethod
    def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()


if __name__ == "__main__":
    WeatherGUI().start()
