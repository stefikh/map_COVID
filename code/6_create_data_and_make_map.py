import plotly
import os
import json
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'Country_and_coord_and_dynFULL_no_text.json')

sample_json = ''
with open(filename, "r", encoding="utf-8") as file:
    sample_json += file.read()

glossary = json.loads(sample_json)
all_countries = {}
new_glossary = {}
#создаем словарь всех стран с координатами
for date in glossary:
    countries = glossary[date]
    for country in countries:
        all_countries[country] = {}
        all_countries[country]["lat"] = countries[country]["lat"]
        all_countries[country]["lon"] = countries[country]["lon"]

loc_glossary = {}           
loc_glossary["lats"] = {}
loc_glossary["lons"] = {}
for country in all_countries:
    loc_glossary["lats"][country] = all_countries[country]["lat"]
    loc_glossary["lons"][country] = all_countries[country]["lon"]
    
for date in glossary:
    new_glossary[date] = {}
    for country in all_countries:
        new_glossary[date][country] = 0

#создаем список всех дат
date_list = []
        
for date in glossary:
    date_list.append(date)
    
countries = glossary[date_list[0]]
for country in countries:
    if countries[country]["dyn"] == 0:
        new_glossary[date_list[0]][country] -= 1
    elif countries[country]["dyn"] == 1:
        new_glossary[date_list[0]][country] += 1

for i in range(1, len(date_list), 1):
    countries = glossary[date_list[i]]
    for country in countries:
        if countries[country]["dyn"] == 0:
            new_glossary[date_list[i]][country] = new_glossary[date_list[i - 1]][country] - 1
        elif countries[country]["dyn"] == 1:
            new_glossary[date_list[i]][country] = new_glossary[date_list[i - 1]][country] + 1
    for place in new_glossary[date_list[i]]:
        if place not in countries:
            new_glossary[date_list[i]][place] = new_glossary[date_list[i - 1]][place]

#превращаем в анимируемый датафрейм страны, дату, динамику. 
#Каждая локация повторяется в списке 873 раза (столько у нас дат), таким образом для каждой страны в каждую дату у нас зафиксирована динамика
df = pd.DataFrame.from_dict(new_glossary)
df = df.stack().reset_index().rename(columns={'level_0':'Место','level_1':'Дата',0:'Динамика'}) 

locdf = pd.DataFrame.from_dict(loc_glossary) # превращаем в отдельный датафрейм координаты
df

#довольно кривенько делаем так, чтобы координаты тоже повторялись по 873 раза (по порядку)

oldlat = locdf['lats'].to_list()

newlat = []

for lat in oldlat:
    for i in range (1, 870):
        newlat.append(lat)
        
oldlon = locdf['lons'].to_list()

newlon = []

for lon in oldlon:
    for i in range (1, 870):
        newlon.append(lon)
        
print(len(newlon))
print(len(newlat))

locdf = locdf.rename_axis('Country').reset_index()
locdf.to_csv('locdataframe.csv')
locdf

#добавляем координаты в общий датафрейм

df["lats"] = newlat
df["lons"] = newlon

df.to_csv('dataframe.csv')
df

#рисуем карту

fig = px.scatter_geo(df, lat="lats",
              lon="lons", animation_frame="Дата", hover_name="Место", color="Динамика", 
                     title = "Карта динамики распространения коронавируса по данным телеграм-канала BBC RUSSIA", 
                     color_continuous_scale=px.colors.sequential.Inferno, range_color=[-12,2])
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 0.0000001
fig.update_layout(height=600, margin={"r":0,"t":30,"l":0,"b":0})
fig.update_geos(
    visible=False, resolution=50,  showland=True, landcolor = '#87decd', oceancolor = 'rgb(202, 252, 2470)', showocean=True,
    showcountries=True, countrycolor="#1b6636"
)
fig.show()
fig.write_html("Map.html")
