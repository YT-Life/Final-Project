from django.shortcuts import render, redirect
from .models import Images

# 만들어 놓은 파이썬 함수(색상 관련 함수, 톤앤톤 톤온톤 관련 함수, yolo에서 exp파일 정리하는 함수)
from static.model.color_function import get_cluster_num, image_color_clustering, cluster_rgb_values, rgb_list_to_hex_list
from static.model.file_function import read_all_file, copy_all_file
from static.model.tone_function import tone_in_tone, tone_on_tone

# 필수 기본 모듈
# os - 프롬프트에서 하는 작업을 파이썬 코드로 실행하기 위해서
# shutil - 디렉토리 강제 삭제(os에서도 디렉토리 삭제 함수가 있으나, 안에 아무것도 없을때만 동작)
# joblib - 학습된 모델 정보 불러오기(색상 군집화 모델(.pkl) 불러옴)
import os, shutil, joblib
import pandas as pd
import sqlite3


# Create your views here.
def mix_color(request):
    if request.method == 'POST':
        img = Images.objects.last()
        color_list = request.POST.getlist('choice')

        if color_list:
            # 팔레트가 가지고 있는 색들에서 유사한 색 추출
            cluster_map = pd.read_csv('static/model/cluster_map.csv')
            # 이미 학습된 데이터를 가져오기 위해 joblib.load 사용 덤프저장
            # 군집 모델인 knn_model.pkl 불러옴
            model = joblib.load('static/model/knn_model.pkl')

            clusterd_color = [] # 유사한 색 리스트
            palette_list = []   # template에 전송할 팔레트 번호

            tone_on_tone_list = []
            tone_in_tone_list = []
            for color in color_list:
                tmp = list(cluster_map[cluster_map['cluster'] == get_cluster_num(color, model)]['hex'])
                # extend - append와는 다르게 리스트형식이 아닌 값이 들어감
                # ex) clusterd_color.extend([1, 2, 3]) = clusterd_color[1, 2, 3]
                # ex) clusterd_color.append([1, 2, 3]) = clusterd_color[[1, 2, 3]]
                clusterd_color.extend(tmp)
                tone_on_tone_list.append(tone_on_tone(color))
                tone_in_tone_list.append(tone_in_tone(color))
            
            tot_content = zip(color_list, tone_on_tone_list)
            tit_content = zip(color_list, tone_in_tone_list)
            
            conn = sqlite3.connect("color.db")
            cursor = conn.cursor()

            for color in clusterd_color:
                cursor.execute(f'''select group_no from color
                                    where color1 = '{color}'
                                    or color2 = '{color}'
                                    or color3 = '{color}'
                                    or color4 = '{color}';''')
                tmp = cursor.fetchall()
                for t in tmp:
                    palette_list.append(t[0])
            
            context = {
                'img' : img,
                'palette_list' : palette_list,
                'color_list' : color_list,
                'tot_content' : tot_content,
                'tit_content' : tit_content,
                # 'tone_on_tone_list' : tone_on_tone_list,
                # 'tone_in_tone_list' : tone_in_tone_list,
            }
            return render(request, 'lyt/mix_color.html', context)
        
        else:
            return redirect('lyt:upload')

    return render(request, 'lyt/mix_color.html')


def upload(request):
    img = Images.objects.last()

    if 'bg_color_list' in request.session and 'ob_color_list' in request.session:
        bg_color_list = request.session['bg_color_list']
        ob_color_list = request.session['ob_color_list']

    context = {
    'img' : img, 
    'bg_color_1' : bg_color_list[0], 'bg_color_2' : bg_color_list[1], 'bg_color_3' : bg_color_list[2], 'bg_color_4' : bg_color_list[3], 'bg_color_5' : bg_color_list[4],
    'ob_color_1' : ob_color_list[0], 'ob_color_2' : ob_color_list[1], 'ob_color_3' : ob_color_list[2], 'ob_color_4' : ob_color_list[3], 'ob_color_5' : ob_color_list[4],
    'ob_color_6' : ob_color_list[5], 'ob_color_7' : ob_color_list[6], 'ob_color_8' : ob_color_list[7], 'ob_color_9' : ob_color_list[8], 'ob_color_10' : ob_color_list[9],
    'ob_color_11' : ob_color_list[10], 'ob_color_12' : ob_color_list[11], 'ob_color_13' : ob_color_list[12], 'ob_color_14' : ob_color_list[13], 'ob_color_15' : ob_color_list[14],
    'ob_color_16' : ob_color_list[15], 'ob_color_17' : ob_color_list[16], 'ob_color_18' : ob_color_list[17], 'ob_color_19' : ob_color_list[18], 'ob_color_20' : ob_color_list[19],
    }
    return render(request, 'lyt/upload.html', context)


def img_upload(request):
    if request.method == 'POST':
        cf = request.FILES.get('chooseFile')
        if cf:
            Images(pic=cf).save()
            # 가장 최신의 데이터를 가져옴
            img = Images.objects.last()

            # path 생성
            # 1. BASE_PATH - 장고 프로젝트 경로
            BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # image path 설정
            # 운영체제(ex 윈도우, 리눅스)에 따른 구분자의 영향을 없애기 위해서 os.path.join을 사용하고
            # os.path.join에 각각을 구분자 없이 요소들을 넣어야 해서 split을 해서 요소 하나하나를 꺼냄
            img_path = img.pic.url.replace('/','\\').split(os.path.sep)

            # * : 리스트 안에 있는 요소들을 알아서 꺼내줌
            image_path = os.path.join(BASE_PATH, *img_path)

            # 배경색 추출 함수 실행
            bg_color_list = image_color_clustering(image_path, clusters=5)
            bg_color_list = rgb_list_to_hex_list(bg_color_list)
            
            # 가구색 추출 함수 실행
            # yolo path
            yolo_path = os.path.join(BASE_PATH, 'static', 'model', 'yolov5-master')
            exp_path = os.path.join(yolo_path,'runs', 'detect', 'exp')
            crop_path = os.path.join(yolo_path,'runs', 'detect', 'exp', 'crops')
            new_ob_path = os.path.join(yolo_path, 'runs', 'detect', 'result')
            
            # 실행할때 위치를 yolo_path로 설정
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
                    # extend - append와는 다르게 리스트형식이 아닌 값이 들어감
                    # ex) clusterd_color.extend([1, 2, 3]) = clusterd_color[1, 2, 3]
                    # ex) clusterd_color.append([1, 2, 3]) = clusterd_color[[1, 2, 3]]
                    ob_color_list.extend(tmp) # ob_color_list = 객체 수 * 20

            # cluster_rgb_values = ob_color_list의 값을 20개로 추리는 함수
            ob_color_list = cluster_rgb_values(ob_color_list)

            # 페이지를 실행할때마다 yolo가 실행되서 기다리는 시간이 많아짐
            # 그래서 데이터를 다른 view에서도 사용할 수 있게끔 request.session을 사용해서 보내줌
            # 이 결과 yolo가 돌아가는 페이지가 있고, 데이터만 담아주는 페이지가 나뉜다.
            request.session['bg_color_list'] = bg_color_list
            request.session['ob_color_list'] = ob_color_list

            return redirect('lyt:upload')
        
        else:
            # messages.warning(request, "이미지를 업로드 해주세요")
            return redirect('lyt:img_upload')

    return render(request, 'lyt/img_upload.html')


def index(request):
    return render(request, 'lyt/index.html')
