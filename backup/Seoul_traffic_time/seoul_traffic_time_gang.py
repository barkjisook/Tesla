#강변북로 시간대별 교통량

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def seoul_traffic_time_gang():

    seoul_traffic = pd.read_excel('./data/노선별 시간대별 교통량(평일).xlsx')
    
    #강변북로 동향
    gang_e = seoul_traffic.iloc[2:,3]

    #강변북로 서향
    gang_w = seoul_traffic.iloc[2:,4]

    #강변북로 동향,서향 통행량 차이
    gang = seoul_traffic.iloc[2:,3:5]
    gang = gang.diff(axis=1)
    gang = gang.abs()
    gang_diff = gang.iloc[:,1]
    gang_diff.values
    gang_diff = gang_diff.values

    #강변북로 통행량 평균
    gang = seoul_traffic.iloc[2:,3:5]
    gang_mean = gang.mean(axis=1)
    gang_mean.values
    gang_mean = gang_mean.values

    #시각화 하기
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
    plt.title('강변북로 시간별 교통량')
    ax1.plot(x, gang_diff, '-s', color='steelblue', markersize=7, linewidth=3, alpha=0.7, label='Diff')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Diff')
    ax1.tick_params(axis='both', direction='in')

    ax2 = ax1.twinx()
    ax2.bar(x, gang_mean, color='lightblue', label='Mean', alpha=0.6, width=0.7)
    ax2.set_ylabel('Traffic')
    ax2.tick_params(axis='y', direction='in')
    ax2.set_ylim(0, 10000)

    ax1.set_zorder(ax2.get_zorder() + 10)
    ax1.patch.set_visible(False)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    return plt.show()