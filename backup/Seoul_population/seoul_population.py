import pandas as pd
import numpy as np
import json
import re
import folium

def seoul_population():
    population = pd.read_excel('./data/인구__가구_및_주택__읍면동_2015_2020___시군구_20162019__20220720180434.xlsx',skiprows=1)
    seoul_population = population.iloc[5:30,:2]
    seoul_population.columns=['name','values']
    geo_json='https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json'
    seoul_population.sort_values(by='name')
    seoul_population['name'] = seoul_population['name'].apply(lambda x: re.compile('[가-힣]+').findall(x)[0])
    m = folium.Map(
        location=[37.566345, 126.977893],
        tiles = 'cartodbpositron'
    )

    folium.Choropleth(
        geo_data = geo_json,
        name = 'choropleth',
        data = seoul_population,
        columns = ['name','values'],
        key_on = 'feature.properties.name',
        fill_color='PuBu',
        fill_opacity=0.7,
        line_opacity=0.2
    ).add_to(m)
    return m

print(seoul_population)