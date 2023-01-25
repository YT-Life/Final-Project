# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Img
from static.model.color_function import get_cluster_num, image_color_clustering, cluster_rgb_values, rgb_list_to_hex_list
from static.model.tone_function import tone_in_tone, tone_on_tone
from static.model.file_function import read_all_file, copy_all_file
import os, shutil, joblib
import pandas as pd
import sqlite3

# main page 
def main(request):
    return render(request, 'jun/main.html')

# file upload
def upload(request):
    form = Img()
    try: 
        # save the image to the model from the request
        form.image=request.FILES['img_file']
        form.save()
        return redirect(reverse("jun:extract"))

    # if there is no image
    except:
        # print("No image")
        # go back to the upload page
        return redirect(reverse("jun:main") + '#upload')
        
# yolo와 군집화 통한 색상 추출
def extract(request):
    # 가장 최신의 데이터를 가져옴
    image = Img.objects.last()

    # path 생성
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # image path 설정
    img_path = image.image.url.replace('/','\\').split(os.path.sep)   # 파일 경로를 구분자 기준으로 분리
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
    os.system(f"python detect.py --source {image_path} --weights ./runs/train/all_objects_200/weights/best.pt --conf 0.01 --save-crop --max-det 6")
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

    return redirect('jun:print_extract')

# 추출한 색상 출력
def print_extract(request):
    image = Img.objects.last()

    if 'bg_color_list' in request.session and 'ob_color_list' in request.session:
        bg_color_list = request.session['bg_color_list']
        ob_color_list = request.session['ob_color_list']

    # print(bg_color_list)
    # print(len(ob_color_list))

    context = {
    'image' : image, 
    'bg_color_1' : bg_color_list[0], 'bg_color_2' : bg_color_list[1], 'bg_color_3' : bg_color_list[2], 'bg_color_4' : bg_color_list[3], 'bg_color_5' : bg_color_list[4],
    'ob_color_1' : ob_color_list[0], 'ob_color_2' : ob_color_list[1], 'ob_color_3' : ob_color_list[2], 'ob_color_4' : ob_color_list[3], 'ob_color_5' : ob_color_list[4],
    'ob_color_6' : ob_color_list[5], 'ob_color_7' : ob_color_list[6], 'ob_color_8' : ob_color_list[7], 'ob_color_9' : ob_color_list[8], 'ob_color_10' : ob_color_list[9],
    'ob_color_11' : ob_color_list[10], 'ob_color_12' : ob_color_list[11], 'ob_color_13' : ob_color_list[12], 'ob_color_14' : ob_color_list[13], 'ob_color_15' : ob_color_list[14],
    'ob_color_16' : ob_color_list[15], 'ob_color_17' : ob_color_list[16], 'ob_color_18' : ob_color_list[17], 'ob_color_19' : ob_color_list[18], 'ob_color_20' : ob_color_list[19],
    }
    return render(request, 'jun/print_extract.html', context)

def recommend(request):
    image = Img.objects.last()

    color_list = request.POST.getlist('choice')

    if color_list:

        # 팔레트가 가지고 있는 색들에서 유사한 색 추출
        cluster_map = pd.read_csv('static/model/cluster_map.csv')
        model = joblib.load('static/model/knn_model.pkl')

        clustered_color = [] # 같은 군집의 색상
        palette_list = []   # template에 전송할 팔레트 번호

        tone_on_tone_list = []
        tone_in_tone_list = []

        for color in color_list:
            tmp = list(cluster_map[cluster_map['cluster'] == get_cluster_num(color, model)]['hex'])
            clustered_color.extend(tmp)
            tone_on_tone_list.append(tone_on_tone(color))
            tone_in_tone_list.append(tone_in_tone(color))
        

        # print(clustered_color)
        # print(tone_on_tone_list)
        # print(tone_in_tone_list)

        conn = sqlite3.connect("color.db")
        cursor = conn.cursor()

        for color in clustered_color:
            cursor.execute(f'''select group_no from color
                                where color1 = '{color}'
                                or color2 = '{color}'
                                or color3 = '{color}'
                                or color4 = '{color}'; ''')
            palette_list.append(cursor.fetchall()[0][0])

        content=zip(color_list,tone_on_tone_list,tone_in_tone_list)  
        # for pair in content:
        #     print(pair)

        context = {
            'image' : image,
            'palette_list' : palette_list,
            'content' : content,
            # 'color_list' : color_list,
            # 'tone_on_tone_list' : tone_on_tone_list,
            # 'tone_in_tone_list' : tone_in_tone_list,
        }

        return render(request, 'jun/recommend.html', context)

    else:
        return redirect('jun:print_extract')
