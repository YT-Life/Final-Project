from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import Images
from static.model.color_function import get_cluster_num, image_color_clustering, cluster_rgb_values, rgb_list_to_hex_list
from static.model.file_function import read_all_file, copy_all_file
import os, shutil, joblib
import pandas as pd
import sqlite3



# Create your views here.


def sso_mainpage (request):
    return render(request, 'sso/sso_main.html')


def sso_upload_index(request):
    if request.method == 'POST':
        cf = request.FILES.get('chooseFile')
        if cf:
            Images(pic=cf).save()
            # 가장 최신의 데이터를 가져옴
            img = Images.objects.last()

            # path 생성
            BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # image path 설정
            img_path = img.pic.url.replace('/','\\').split(os.path.sep)   # 파일 경로를 구분자 기준으로 분리
            image_path = os.path.join(BASE_PATH, *img_path) # os.path.join을 통해 운영체제에 맞는 경로 생성
            # yolo path 설정
            yolo_path = os.path.join(BASE_PATH, 'static', 'model', 'yolov5-master')
            exp_path = os.path.join(yolo_path,'runs', 'detect', 'exp')
            crop_path = os.path.join(yolo_path,'runs', 'detect', 'exp', 'crops')
            new_ob_path = os.path.join(yolo_path, 'runs', 'detect', 'result')

            # 배경색 추출 함수 실행
            bg_color_list = image_color_clustering(image_path, clusters=5)
            bg_color_list = rgb_list_to_hex_list(bg_color_list)
            
            
            # 실행
            os.chdir(yolo_path)
            # exp파일 제거
            if os.path.exists(exp_path):
                shutil.rmtree(exp_path)
            os.system(f"python detect.py --source {image_path} --weights ./runs/train/all_objects_200/weights/best.pt --conf 0.01 --save-crop --max-det 4")
            os.chdir(BASE_PATH)

            # src_path 안에 모든 파일들 new_path로 복사하여 저장
            # result 파일 refresh
            if os.path.exists(new_ob_path):
                shutil.rmtree(new_ob_path)
                os.mkdir(new_ob_path)
            # 파일 옮기기
            if os.path.exists(crop_path):
                file_list = read_all_file(crop_path)
                copy_all_file(file_list, new_ob_path)
            # exp파일 제거
            if os.path.exists(exp_path):
                shutil.rmtree(exp_path)
                
            # 가구색 추출 함수
            object_list = os.listdir(new_ob_path)
            ob_color_list = []
            if len(object_list):
                for object in object_list:
                    object_path = os.path.join(new_ob_path, object)
                    tmp = image_color_clustering(object_path)
                    ob_color_list.extend(tmp)

            ob_color_list = cluster_rgb_values(ob_color_list)

            request.session['bg_color_list'] = bg_color_list
            request.session['ob_color_list'] = ob_color_list

            return redirect('sso:extract_color')
        else:
            return redirect('sso:upload_index')
    return render(request, 'sso/sso_upload_index.html')

def sso_extract_color (request):
    # 가장 최근의 데이터를 가져옴.
    image = Images.objects.last()

    if 'bg_color_list' in request.session and 'ob_color_list' in request.session:
        bg_color_list = request.session['bg_color_list']
        ob_color_list = request.session['ob_color_list']

    context = {
    'image' : image, 
    'bg_color_1' : bg_color_list[0], 'bg_color_2' : bg_color_list[1], 'bg_color_3' : bg_color_list[2], 'bg_color_4' : bg_color_list[3], 'bg_color_5' : bg_color_list[4],
    'ob_color_1' : ob_color_list[0], 'ob_color_2' : ob_color_list[1], 'ob_color_3' : ob_color_list[2], 'ob_color_4' : ob_color_list[3], 'ob_color_5' : ob_color_list[4],
    'ob_color_6' : ob_color_list[5], 'ob_color_7' : ob_color_list[6], 'ob_color_8' : ob_color_list[7], 'ob_color_9' : ob_color_list[8], 'ob_color_10' : ob_color_list[9],
    'ob_color_11' : ob_color_list[10], 'ob_color_12' : ob_color_list[11], 'ob_color_13' : ob_color_list[12], 'ob_color_14' : ob_color_list[13], 'ob_color_15' : ob_color_list[14],
    'ob_color_16' : ob_color_list[15], 'ob_color_17' : ob_color_list[16], 'ob_color_18' : ob_color_list[17], 'ob_color_19' : ob_color_list[18], 'ob_color_20' : ob_color_list[19],
    }
    return render(request, 'sso/sso_extract_color.html', context)

def sso_best_color_palette (request):
    if request.method == 'POST':
        image = Images.objects.last()
        color_list = request.POST.getlist('choice')
        
        if color_list:
            # 팔레트가 가지고 있는 색들에서 유사한 색 추출
            cluster_map = pd.read_csv('static/model/cluster_map.csv')
            model = joblib.load('static/model/knn_model.pkl')
            clusterd_color = [] # 유사한 색 리스트
            palette_list = []   # template에 전송할 팔레트 번호

            for color in color_list:
                tmp = list(cluster_map[cluster_map['cluster'] == get_cluster_num(color, model)]['hex'])
                clusterd_color.extend(tmp)
                
            print(clusterd_color)
            
            conn = sqlite3.connect("color.db")
            cursor = conn.cursor()

            for color in clusterd_color:
                cursor.execute(f'''select group_no from color
                                    where color1 = '{color}'
                                    or color2 = '{color}'
                                    or color3 = '{color}'
                                    or color4 = '{color}';''')
                palette_list.append(cursor.fetchall()[0][0])

            # print(palette_list)
            context = {
                'image' : image,
                'color_list' : color_list,
                'palette_list' : palette_list,
            }
            return render (request, 'sso/sso_best_color_palette.html', context)
        else:
            return redirect('sso:extract_color')
    return render(request, 'sso/sso_best_color_palette.html', context)

