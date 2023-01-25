import pandas as pd
import numpy as np
from PIL import ImageColor
import cv2
import colorsys
import joblib
import warnings
warnings.filterwarnings(action='ignore')
from sklearn.cluster import KMeans


# 색상값 hue 범주화 (360도를 15도씩 나눠서 범주화)
def classify_hue(df):
    df.loc[:, 'hue_class'] = np.nan
    df.loc[(df['hue']*360 >= 0) & (df['hue']*360 < 15), 'hue_class'] = 1
    df.loc[(df['hue']*360 >= 15) & (df['hue']*360 < 30), 'hue_class'] = 2
    df.loc[(df['hue']*360 >= 30) & (df['hue']*360 < 45), 'hue_class'] = 3
    df.loc[(df['hue']*360 >= 45) & (df['hue']*360 < 60), 'hue_class'] = 4
    df.loc[(df['hue']*360 >= 60) & (df['hue']*360 < 75), 'hue_class'] = 5
    df.loc[(df['hue']*360 >= 75) & (df['hue']*360 < 90), 'hue_class'] = 6
    df.loc[(df['hue']*360 >= 90) & (df['hue']*360 < 105), 'hue_class'] = 7
    df.loc[(df['hue']*360 >= 105) & (df['hue']*360 < 120), 'hue_class'] = 8
    df.loc[(df['hue']*360 >= 120) & (df['hue']*360 < 135), 'hue_class'] = 9
    df.loc[(df['hue']*360 >= 135) & (df['hue']*360 < 150), 'hue_class'] = 10
    df.loc[(df['hue']*360 >= 150) & (df['hue']*360 < 165), 'hue_class'] = 11
    df.loc[(df['hue']*360 >= 165) & (df['hue']*360 < 180), 'hue_class'] = 12
    df.loc[(df['hue']*360 >= 180) & (df['hue']*360 < 195), 'hue_class'] = 13
    df.loc[(df['hue']*360 >= 195) & (df['hue']*360 < 210), 'hue_class'] = 14
    df.loc[(df['hue']*360 >= 210) & (df['hue']*360 < 225), 'hue_class'] = 15
    df.loc[(df['hue']*360 >= 225) & (df['hue']*360 < 240), 'hue_class'] = 16
    df.loc[(df['hue']*360 >= 240) & (df['hue']*360 < 255), 'hue_class'] = 17
    df.loc[(df['hue']*360 >= 255) & (df['hue']*360 < 270), 'hue_class'] = 18
    df.loc[(df['hue']*360 >= 270) & (df['hue']*360 < 285), 'hue_class'] = 19
    df.loc[(df['hue']*360 >= 285) & (df['hue']*360 < 300), 'hue_class'] = 20
    df.loc[(df['hue']*360 >= 300) & (df['hue']*360 < 315), 'hue_class'] = 21
    df.loc[(df['hue']*360 >= 315) & (df['hue']*360 < 330), 'hue_class'] = 22
    df.loc[(df['hue']*360 >= 330) & (df['hue']*360 < 345), 'hue_class'] = 23
    df.loc[(df['hue']*360 >= 345) & (df['hue']*360 < 360), 'hue_class'] = 24
    return df

# 채도값 sat 범주화 (0.05단위)
def classify_sat(df):
    df.loc[:, 'sat_class'] = np.nan
    df.loc[(df['sat'] >= 0) & (df['sat'] < 0.05), 'sat_class'] = 0
    df.loc[(df['sat'] >= 0.05) & (df['sat'] < 0.10), 'sat_class'] = 0.5
    df.loc[(df['sat'] >= 0.10) & (df['sat'] < 0.15), 'sat_class'] = 1.0
    df.loc[(df['sat'] >= 0.15) & (df['sat'] < 0.20), 'sat_class'] = 1.5
    df.loc[(df['sat'] >= 0.20) & (df['sat'] < 0.25), 'sat_class'] = 2.0
    df.loc[(df['sat'] >= 0.25) & (df['sat'] < 0.30), 'sat_class'] = 2.5
    df.loc[(df['sat'] >= 0.30) & (df['sat'] < 0.35), 'sat_class'] = 3.0
    df.loc[(df['sat'] >= 0.35) & (df['sat'] < 0.40), 'sat_class'] = 3.5
    df.loc[(df['sat'] >= 0.40) & (df['sat'] < 0.45), 'sat_class'] = 4.0
    df.loc[(df['sat'] >= 0.45) & (df['sat'] < 0.50), 'sat_class'] = 4.5
    df.loc[(df['sat'] >= 0.50) & (df['sat'] < 0.55), 'sat_class'] = 5.0
    df.loc[(df['sat'] >= 0.55) & (df['sat'] < 0.60), 'sat_class'] = 5.5
    df.loc[(df['sat'] >= 0.60) & (df['sat'] < 0.65), 'sat_class'] = 6.0
    df.loc[(df['sat'] >= 0.65) & (df['sat'] < 0.70), 'sat_class'] = 6.5
    df.loc[(df['sat'] >= 0.70) & (df['sat'] < 0.75), 'sat_class'] = 7.0
    df.loc[(df['sat'] >= 0.75) & (df['sat'] < 0.80), 'sat_class'] = 7.5
    df.loc[(df['sat'] >= 0.80) & (df['sat'] < 0.85), 'sat_class'] = 8.0
    df.loc[(df['sat'] >= 0.85) & (df['sat'] < 0.90), 'sat_class'] = 8.5
    df.loc[(df['sat'] >= 0.90) & (df['sat'] < 0.95), 'sat_class'] = 9.0
    df.loc[(df['sat'] >= 0.95) & (df['sat'] <= 1.0), 'sat_class'] = 9.5
    return df

# 명도값 val 범주화 (0.05단위)
def classify_val(df):
    df.loc[:, 'val_class'] = np.nan
    df.loc[(df['val'] >= 0) & (df['val'] < 0.05), 'val_class'] = 0
    df.loc[(df['val'] >= 0.05) & (df['val'] < 0.10), 'val_class'] = 0.5
    df.loc[(df['val'] >= 0.10) & (df['val'] < 0.15), 'val_class'] = 1.0
    df.loc[(df['val'] >= 0.15) & (df['val'] < 0.20), 'val_class'] = 1.5
    df.loc[(df['val'] >= 0.20) & (df['val'] < 0.25), 'val_class'] = 2.0
    df.loc[(df['val'] >= 0.25) & (df['val'] < 0.30), 'val_class'] = 2.5
    df.loc[(df['val'] >= 0.30) & (df['val'] < 0.35), 'val_class'] = 3.0
    df.loc[(df['val'] >= 0.35) & (df['val'] < 0.40), 'val_class'] = 3.5
    df.loc[(df['val'] >= 0.40) & (df['val'] < 0.45), 'val_class'] = 4.0
    df.loc[(df['val'] >= 0.45) & (df['val'] < 0.50), 'val_class'] = 4.5
    df.loc[(df['val'] >= 0.50) & (df['val'] < 0.55), 'val_class'] = 5.0
    df.loc[(df['val'] >= 0.55) & (df['val'] < 0.60), 'val_class'] = 5.5
    df.loc[(df['val'] >= 0.60) & (df['val'] < 0.65), 'val_class'] = 6.0
    df.loc[(df['val'] >= 0.65) & (df['val'] < 0.70), 'val_class'] = 6.5
    df.loc[(df['val'] >= 0.70) & (df['val'] < 0.75), 'val_class'] = 7.0
    df.loc[(df['val'] >= 0.75) & (df['val'] < 0.80), 'val_class'] = 7.5
    df.loc[(df['val'] >= 0.80) & (df['val'] < 0.85), 'val_class'] = 8.0
    df.loc[(df['val'] >= 0.85) & (df['val'] < 0.90), 'val_class'] = 8.5
    df.loc[(df['val'] >= 0.90) & (df['val'] < 0.95), 'val_class'] = 9.0
    df.loc[(df['val'] >= 0.95) & (df['val'] <= 1.0), 'val_class'] = 9.5
    return df

# 범주화된 데이터 프레임 반환 함수
def color_clustering(df, k):
    # group 칼럼이 있으면 이를 제거
    if 'group' in df.columns:
        df.drop(['group'], axis=1, inplace=True)
        
    # 중복된 색체 값 제거
    df = df.drop_duplicates(ignore_index=True)
    
    # hue, sat, val값 범주화
    df = classify_hue(df)
    df = classify_sat(df)
    df = classify_val(df)
    
    # 클러스터링에 필요없는 변수 제거
    if 'hue' in df.columns:
        df.drop(['hue'], axis=1, inplace=True)
    if 'sat' in df.columns:
        df.drop(['sat'], axis=1, inplace=True)
    if 'val' in df.columns:
        df.drop(['val'], axis=1, inplace=True)
        
    # RGB값을 0과 1사이의 값으로 변환
    df['red'] = round(df['red']/255, 3)
    df['green'] = round(df['green']/255, 3)
    df['blue'] = round(df['blue']/255, 3)
    
    hex_col = df['hex']
    df.drop(['hex'], axis=1, inplace=True)

    # 모델학습
    model = KMeans(n_clusters=k, random_state=42)
    model.fit(df)
    
    # 군집화 데이터 프레임 
    cluster_map = pd.DataFrame()
    cluster_map['data_index'] = df.index.values
    cluster_map['hex'] = hex_col
    cluster_map['cluster'] = model.labels_
    
    # 모델 저장
    joblib.dump(model, 'knn_model.pkl')

    # 클러스터맵 저장
    cluster_map.to_csv('cluster_map.csv', index=False)

# -----------------------------------------------------------------
# find similar color by cluster
# -----------------------------------------------------------------
def get_cluster_num(hex_value, model):
    
    # 색상 hex 값에서 #이 없다면 이를 더함
    if '#' not in hex_value[0]:
        hex_value = '#' + hex_value
    
    # rgb값 계산
    red = round(ImageColor.getcolor(hex_value, 'RGB')[0]/255, 3)
    green = round(ImageColor.getcolor(hex_value, 'RGB')[1]/255, 3)
    blue = round(ImageColor.getcolor(hex_value, 'RGB')[2]/255, 3)
    
    # hsv값 계산
    hue = round(colorsys.rgb_to_hsv(red, green, blue)[0], 3)
    sat = round(colorsys.rgb_to_hsv(red, green, blue)[1], 3)
    val = round(colorsys.rgb_to_hsv(red, green, blue)[2], 3)

    # 데이터 프레임으로 변경해야 앞선 전처리 함수가 작동
    input_color = pd.DataFrame({'red': [red], 
                                'green':[green], 
                                'blue':[blue], 
                                'hue': [hue], 
                                'sat':[sat], 
                                'val':[val]})

    input_color = classify_hue(input_color)
    input_color = classify_sat(input_color)
    input_color = classify_val(input_color)
    
    # hue, sat, val 변수 제거
    input_color = input_color.drop(['hue', 'sat', 'val'], axis=1)

    cluster_num = model.predict(input_color)[0]

    return cluster_num

# 메인실행
# cluster_map = pd.read_csv('./data/cluster_map.csv')
# new_color = '#EEEEEE'
# model = joblib.load('./data/knn_model.pkl')
# cluster_map[cluster_map['cluster'] == get_cluster_num(new_color, model)]


# -----------------------------------------------------------------
# transform list to hex (value, list)
# -----------------------------------------------------------------
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def rgb_list_to_hex_list(rgb_list):
    color_list = []
    for color in rgb_list:
        red, green, blue = int(color[0]), int(color[1]), int(color[2])
        color_list.append('#'+rgb_to_hex((red, green, blue)))
    return color_list

# -----------------------------------------------------------------
# color extraction from image
# -----------------------------------------------------------------
def image_color_clustering(image, clusters=20, rounds=1):
        """
        Parameters
            image <np.ndarray> : 이미지
            clusters <int> : 클러스터 개수
            rounds <int> : 알고리즘 반복 횟수 (보통 1)
        returns
            color_list : 군집화 완료된 색상의 hex값
        """
        image = cv2.imread(image) # BGR값을 출력
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # BGR값을 RGB값으로 변형

        height, width = image.shape[:2]
        samples = np.zeros([ height * width, 3 ], dtype=np.float32)
        
        count = 0
        for x in range(height):
            for y in range(width):
                samples[count] = image[x][y]
                count += 1
        
        compactness, labels, centers = cv2.kmeans( # cs2.kmeans - 이미지에 있는 색상을 kmeans(군집화) 해줌
                    samples, # 비지도 학습 데이터 정렬
                    clusters, # 군집화 개수
                    None, # 각 샘플의 군집 번호 정렬
                    # criteria : kmeans 알고리즘 반복 종료 기준 설정
                    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 
                                10000, # max_iter 
                                0.0001), # epsilon 
                    # attempts : 다른 초기 중앙값을 이용해 반복 실행할 횟수
                    attempts = rounds, 
                    # flags : 초기 중앙값 설정 방법
                    flags = cv2.KMEANS_PP_CENTERS)
        
        centers = np.uint8(centers).tolist()
        # centers = rgb_list_to_hex_list(centers)

        return centers


# 메인실행
# image_path = '이미지 경로'
# color_list = image_color_clustering(image_path, k=추출할 색의 수)
# print(color_list)

# -----------------------------------------------------------------
# clustering rgb values
# -----------------------------------------------------------------
def cluster_rgb_values(rgb_list , clusters=20):
    model = KMeans(clusters) # 20개의 중앙값 추출
    model.fit(rgb_list)    
    # 값이 실수값으로 나와서 np.uint8을 이용해서 정수로 변경
    # 현재는 데이터프레임에 시리즈타입이여서 타입을 설명해주는 정보를 버리기위해
    # tolist를 사용해서 시리즈에 있는 요소들만 리스트로 꺼내옴
    centers = np.uint8(model.cluster_centers_).tolist()
    # 리스트로 꺼내온 데이터들은 rgb값이고 이것을 hex값으로 변경
    centers = rgb_list_to_hex_list(centers)
    return centers


