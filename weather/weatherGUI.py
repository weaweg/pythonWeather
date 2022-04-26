import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import ttk
from weather import WeatherApi


class WeatherGUI:
    pd = "15 15 15 15"

    def __init__(self):
        root = tk.Tk()
        root.eval('tk::PlaceWindow . center')
        self.__data__ = WeatherApi()
        self.__city__ = tk.StringVar()
        self.__country__ = tk.StringVar()

        searchFrame = ttk.Frame(root, padding=self.pd)
        dataFrame = ttk.Frame(root, padding=self.pd)
        dataFrame.grid(column=0)
        searchFrame.grid(row=0)

        ttk.Label(searchFrame, text="Miasto").grid(column=1, row=1)
        cityEntry = ttk.Entry(searchFrame, textvariable=self.__city__)
        cityEntry.grid(column=1, row=2)

        ttk.Label(searchFrame, text="Państwo").grid(column=3, row=1)
        countryEntry = ttk.Entry(searchFrame, textvariable=self.__country__)
        countryEntry.grid(column=3, row=2)

        ttk.Button(searchFrame, text="Szukaj", command=self.getCityLocation).grid(column=4, row=2)

        root.title("WeatherApp 2022 by BudzowskiB")
        tk.mainloop()

    def getCityLocation(self):
        cities = WeatherApi.getCityLocation(self.__city__.get(), self.__country__.get())
        if cities is None:
            msgbox.showinfo("Informacja", "Nie znaleziono miasta")
        else:
            pickCity = tk.Tk()
            pickCity.eval("tk::PlaceWindow . center")
            cityTreeView = ttk.Treeview(pickCity, padding=self.pd)
            cityTreeView["columns"] = ("Name", "State", "Country", "Lat", "Lon")
            for city in cities:
                cityTreeView.insert('', tk.END, values=city)
            cityTreeView.grid(row=0)





