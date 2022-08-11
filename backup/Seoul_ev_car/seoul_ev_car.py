import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def seoul_ev_car():
    ev_car = pd.read_csv('./data/한국전력공사_지역별 전기차 현황정보_20220429.csv')
    ev_car = ev_car.sort_index(ascending=False)
    ev_car_2019 = ev_car.iloc[:11,:2]
    ev_car_2020 = ev_car.iloc[11:23,:2]
    ev_car_2021 = ev_car.iloc[23:35,:2]
    ev_car_2022 = ev_car.iloc[35:38,:2]

    #평균 데이터 값
    ev_car_2019_mean = ev_car_2019['서울'].mean()
    ev_car_2020_mean = ev_car_2020['서울'].mean()
    ev_car_2021_mean = ev_car_2021['서울'].mean()
    ev_car_2022_mean = ev_car_2022['서울'].mean()

    #시각화
    x = np.arange(4)
    years = ['2019', '2020', '2021','2022']
    values = [ev_car_2019_mean,ev_car_2020_mean,ev_car_2021_mean,ev_car_2022_mean]

    plt.bar(x, values, width=0.8)
    plt.xticks(x, years)
    plt.title('SEOUL EV Car (2019-2022)')
    plt.xlabel('date')
    plt.ylabel('Evcar')
    return plt.show()