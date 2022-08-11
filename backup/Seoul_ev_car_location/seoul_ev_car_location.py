import pandas as pd
import mapboxgl
from mapboxgl.viz import *
import os
from mapboxgl.utils import df_to_geojson
import json
import folium

def seoul_ev_car_location():
    #데이터 불러오기
    ev_charger = pd.read_csv('./data/한국전력공사_전기차충전소위경도_20220718.csv')
    ev_charger_location = ev_charger[ev_charger['시도'] == '서울특별시']
    # csv -> json
    geo_data = df_to_geojson(
        df = ev_charger_location,
        lat = '위도',
        lon = '경도',
        filename = './data/seoul_ev_charger_location.geojson')

    geo_data = './data/seoul_ev_charger_location.geojson'

    with open(geo_data) as f:
        data = json.loads(f.read())
        location = []

    for i in range(len(data['features'])):
        location.append(data['features'][i]['geometry']['coordinates'])
    
    # folium 시각화
    center = [37.541, 126.986]
    m = folium.Map(location = center, zoom_start=10, tiles='cartodbpositron')
    for i in location:
        folium.Circle(location=i, radius=20, color='skyBlue').add_to(m)
    return m