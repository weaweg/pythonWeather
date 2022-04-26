import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk

from weather import WeatherApi

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np


class WeatherGUI:
    __pd__ = "15 5"

    def __init__(self):
        self.__root__ = tk.Tk()
        self.__root__.resizable(False, False)
        self.__root__.title("WeatherApp 2022 by BudzowskiB")
        self.__root__.eval('tk::PlaceWindow . center')
        self.__weatherApi__ = WeatherApi()
        self.__forecastData__ = None
        self.__cityInput__ = tk.StringVar()
        self.__countryInput__ = tk.StringVar()
        self.__daysInput__ = tk.StringVar()

        self.__initGUI__()

    def __initGUI__(self):
        searchFrame = ttk.Frame(self.__root__, padding=self.__pd__)
        searchFrame.grid(row=0)

        ttk.Label(searchFrame, text="Miasto").grid(column=0, row=0)
        cityEntry = ttk.Entry(searchFrame, textvariable=self.__cityInput__)
        cityEntry.grid(column=0, row=1)

        ttk.Label(searchFrame, text="Państwo").grid(column=1, row=0)
        countryEntry = ttk.Entry(searchFrame, textvariable=self.__countryInput__)
        countryEntry.grid(column=1, row=1)

        ttk.Button(searchFrame, text="Szukaj", command=self.__getCityLocation__).grid(column=2, row=1)

        self.__dataFrame__ = ttk.Frame(self.__root__, padding=self.__pd__)
        self.__dataFrame__.grid(row=1)
        dataLabel = ttk.Label(self.__dataFrame__, text="Wybierz miasto aby wyświetlić pogodę")
        dataLabel.pack()

        optionFrame = ttk.Frame(self.__root__, padding=self.__pd__)
        optionFrame.grid(row=2)
        ttk.Button(optionFrame, text="Poprzedni dzień", command=None).grid(row=0, column=0)
        ttk.Button(optionFrame, text="Następny dzień", command=None).grid(row=0, column=1)

        tk.mainloop()

    def __getCityLocation__(self):
        # cities = WeatherApi.getCityLocation(self.__cityInput__.get(), self.__countryInput__.get())
        cities = [{"name": "custom", "state": "custom", "country": "custom", "lat": 50.235, "lon": 50.125}]
        if cities is None:
            msgbox.showinfo("Informacja", "Nie znaleziono miasta")
        else:
            pickCity = tk.Toplevel()
            self.__root__.eval(f'tk::PlaceWindow {str(pickCity)} center')
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
            ttk.Button(pickCity, text="Wybierz", command=lambda: self.__setCity__(pickCity, cityTreeView, cities)) \
                .grid(column=2, row=2)

    def __setCity__(self, pickCity, cityTreeView, cities):
        index = cityTreeView.index(cityTreeView.focus())
        self.__weatherApi__.setCity(cities[index]["lat"], cities[index]["lon"])
        pickCity.destroy()
        self.__showForecast__()

    def __showForecast__(self):
        self.__forecastData__ = self.__weatherApi__.getForecastWeather()
        if self.__forecastData__ is None:
            msgbox.showerror("Błąd", "Błąd pobierania danych")
            return
        self.__dataFrame__.winfo_children()[0].destroy()

        fig = Figure(figsize=(10, 4), dpi=100)
        t = np.arange(0, 3, .01)
        ax = fig.add_subplot()
        ax.plot(t, 2 * np.sin(2 * np.pi * t))
        ax.set_xlabel("time [s]")
        ax.set_ylabel("f(t)")

        canvas = FigureCanvasTkAgg(fig, master=self.__dataFrame__)
        canvas.draw()
        canvas.get_tk_widget().pack()
