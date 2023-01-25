import os
import shutil

def read_all_file(path):
    output = os.listdir(path)  
    file_list = []
    for i in output:
        if os.path.isdir(os.path.join(path, i)): 
            file_list.extend(read_all_file(os.path.join(path, i))) 
        elif os.path.isfile(os.path.join(path, i)):
            file_list.append(os.path.join(path, i))
    return file_list

def copy_all_file(file_list, new_path):
    i = 1
    for src_path in file_list:
        file = src_path.replace('/','\\').split(os.path.sep)[-1]
        shutil.copyfile(src_path, os.path.join(new_path, file))
        # 객체가 생성됬을때 저장되는 이름이 다 같아서 result폴더에 파일들이 덮어씌어지면서 하나만 남음
        # 이 현상을 막기 위해 각 파일들의 이름 앞에 1~n값을 붙여줌
        os.rename(os.path.join(new_path, file), os.path.join(new_path, str(i)+'_'+file))
        i+=1

