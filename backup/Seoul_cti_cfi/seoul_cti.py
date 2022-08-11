#서울 도로 혼잡시간강도

import pandas as pd
import numpy as np
import json
import requests
import os
from mapboxgl.utils import df_to_geojson
import folium
import networkx as nx

#위경도 값 뽑기(Kakao API 사용)
api_key='05c5e5b93822c0acd93e8cea0015ca13'

def addr_to_lat_lon(addr):
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={address}'.format(address=addr)
    headers = {"Authorization": "KakaoAK " + api_key}
    result = json.loads(str(requests.get(url, headers=headers).text))
    
    #혹시나 해서 오류처리(오류없음)
    if result['documents'] == []:
        return (37.565,126.986)
    else :
        match_first = result['documents'][0]['address']
    
    if  match_first == None:
        #n = result['documents'][0]['road_address']['building_name']
        #result = getXY_Keyword(n)
        return (37.565,126.986)

    return float(match_first['y']), float(match_first['x'])

def seoul_cti():

    #서울 도로망(전국 도로망 데이터 이용, 서울 값만 사용)
    nodes = pd.read_csv('./data/Seoul_nodes.csv')
    links = pd.read_csv('./data/Seoul_links.csv')
    
    nodes = nodes[['Id','NODE_NAME','latitude','longitude']]
    links = links[['Source','Target']]

    source_in = links['Source'].apply(lambda x : x in list(nodes['Id'])) #서울 값만 가져오기
    target_in = links['Target'].apply(lambda x : x in list(nodes['Id'])) #서울 값만 가져오기
    seoul_links = links[source_in & target_in]

    #G = nx.Graph() 명령어를 통해 빈 그래프(네트워크)를 생성
    G = nx.Graph()
    #R == 지구 반지름
    R = 6371e3
    
    for idx,row in nodes.iterrows():
        #Graph G에 node 추가
        G.add_node(row['Id'],Label=row['NODE_NAME'],latitude=row['latitude'], longitude=row['longitude'])
    
    for idx,row in seoul_links.iterrows():
        #Source 와 Target node 사이 계산
        lon1 = float(nodes[nodes['Id'] == row['Source']]['longitude'] * np.pi/180)
        lat1 = float(nodes[nodes['Id'] == row['Source']]['latitude'] * np.pi/180)
        lon2 = float(nodes[nodes['Id'] == row['Target']]['longitude'] * np.pi/180)
        lat2 = float(nodes[nodes['Id'] == row['Target']]['latitude'] * np.pi/180)
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        a = np.sin(d_lat/2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(d_lon/2) ** 2
        c = 2 * np.arctan2(a**0.5, (1-a) ** 0.5)
        d = R * c
        
        #Link attribute : 'Source', 'Target' and weight = 'Length between them'
        G.add_edge(row['Source'],row['Target'],weight = d)

    #중간 위경도 값 (37.60842435049369, 126.95675015496396)
    std_point = tuple(nodes.head(1)[['latitude','longitude']].iloc[0])

    #서울 도로 혼잡시간강도 데이터 전처리
    traffic_time = pd.read_csv('./data/2018년_혼잡시간강도_읍면동.csv')
    seoul_traffic_time = traffic_time[traffic_time['시도명'] == '서울특별시']
    seoul_traffic_time_top50 = seoul_traffic_time.nlargest(50,['혼잡시간강도'])
    seoul_cti = seoul_traffic_time_top50.iloc[:,1:6]
    seoul_cti.drop(['평일주말구분'], axis=1, inplace=True)
    seoul_cti_addr = seoul_cti.iloc[:,2]

    addr_list = []
    for i in seoul_cti_addr:
        addr_list.append(i)

    lat_addr = []
    lon_addr = []
    for i in addr_list:
        lat_addr.append(addr_to_lat_lon(i)[1])
        lon_addr.append(addr_to_lat_lon(i)[0])
    
    cti_lat_lon = pd.DataFrame({
    '위도': lat_addr,
    '경도': lon_addr}, columns=['위도','경도'])
    seoul_cti = seoul_cti.reset_index()
    seoul_cti = pd.concat([seoul_cti, cti_lat_lon], axis=1)

    #csv -> json
    geo_data = df_to_geojson(
        df = seoul_cti,
        lat = '위도',
        lon = '경도',
        filename = './data/seoul_cti.geojson')

    geo_data = './data/seoul_cti.geojson'
    with open(geo_data) as f:
        data = json.loads(f.read())

    location = []
    for i in range(len(data['features'])):
        location.append(data['features'][i]['geometry']['coordinates'])

    cti = []
    for i in range(len(data['features'])):
        cti.append(data['features'][i]['properties']['혼잡시간강도'])
    
    #서울 도로망 및 혼잡시간강도 시각화
    map_osm = folium.Map(location=std_point, zoom_start=10,tiles='cartodbpositron') 

    kw = {'opacity': 0.5, 'weight': 2}
    for ix, row in seoul_links.iterrows():
        start = tuple(nodes[nodes['Id']==row['Source']][['latitude','longitude']].iloc[0])
        end = tuple(nodes[nodes['Id']==row['Target']][['latitude','longitude']].iloc[0])
        folium.PolyLine(
            locations=[start, end],
            color='lightblue',
            line_cap='round',
            **kw,
        ).add_to(map_osm)
        
    for i,j in enumerate(location):
        folium.Circle(location=j, radius=cti[i]*10, color='white',weight=1,fill_opacity=0.6, opacity=1, fill_color='steelblue', fill=True).add_to(map_osm)
        
    return map_osm
    




