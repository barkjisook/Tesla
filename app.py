# app.py
from flask import Flask, render_template
import folium
import pandas as pd
import re
#from mapboxgl.utils import df_to_geojson
import json
import numpy as np
#import matplotlib.pyplot as plt
#plt.switch_backend('agg')
from io import BytesIO
import urllib
import base64
import warnings
warnings.simplefilter("ignore")
import requests
#import networkx as nx

app = Flask(__name__) 

# 1. 메인
@app.route('/') #접속 url
def index():
    return render_template('index.html')

# 2. 팀소개
@app.route('/team')
def team():
    return render_template('team.html')

# 3. 전기차 증가 추이
@app.route('/car')
def car():
    return render_template('car.html')

# 4. 서울시 인구 분포도
@app.route('/pop')
def pop():
    return render_template('pop.html')

# 5. 도로 혼잡 분석
# 5-1. 혼잡빈도강도
@app.route('/cfi')
def cfi():
    return render_template('cfi.html')

# 5-2. 혼잡시간강도
@app.route('/cti')
def cti():
    return render_template('cti.html')

# 6. 도로 통행량
@app.route('/traffic')
def traffic():
    return render_template('traffic.html')

# 7. 충전소 위치
@app.route('/spot')
def spot():
    return render_template('spot.html')

if __name__=="__main__":
    app.run(debug=True)