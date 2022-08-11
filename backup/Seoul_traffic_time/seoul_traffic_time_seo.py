#서부간선도로 시간대별 교통량

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def seoul_traffic_time_seo():
    seoul_traffic = pd.read_excel('./data/노선별 시간대별 교통량(평일).xlsx')

    #서부간선도로 북향
    seo_n = seoul_traffic.iloc[2:,15]

    #서부간선도로 남향
    seo_s = seoul_traffic.iloc[2:,16]

    #서부간선도로 북향,남향 통행량 차이
    seo= seoul_traffic.iloc[2:,15:17]
    seo = seo.diff(axis=1)
    seo = seo.abs()
    seo_diff = seo.iloc[:,1]
    seo_diff = seo_diff.values

    #서부간선도로 통행량 평균
    seo = seoul_traffic.iloc[2:,13:15]
    seo_mean = seo.mean(axis=1)
    seo_mean = seo_mean.values
    
    #시각화하기
    # 1. 기본 스타일 설정
    plt.style.use('default')
    plt.rcParams['figure.figsize'] = (4, 3)
    plt.rcParams['font.size'] = 8
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] =False

    # 2. 데이터 준비
    x = np.arange(24)
    time = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

    # 3. 그래프 그리기
    fig, ax1 = plt.subplots()
    plt.title('서부간선도로 시간별 교통량')
    ax1.plot(x, seo_diff, '-s', color='steelblue', markersize=7, linewidth=3, alpha=0.7, label='Diff')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Diff')
    ax1.tick_params(axis='both', direction='in')

    ax2 = ax1.twinx()
    ax2.bar(x, seo_mean, color='lightblue', label='Mean', alpha=0.6, width=0.7)
    ax2.set_ylabel('Traffic')
    ax2.tick_params(axis='y', direction='in')
    ax2.set_ylim(0, 10000)

    ax1.set_zorder(ax2.get_zorder() + 10)
    ax1.patch.set_visible(False)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    return plt.show()