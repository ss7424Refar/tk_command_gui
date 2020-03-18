import os
import shutil


def mkdir(path1):
    if os.path.exists(path1):
        print(path1 + ' 已经存在')
    else:
        print('创建 ' + path1)
        os.makedirs(path1)


# 返回当前目录
path = os.getcwd()
print('当前目录为：' + path)

# 生成目录
annotation_path = path + '/output/Annotations/'
image_sets_path = path + '/output/ImageSets/Main'
jpeg_path = path + '/output/JPEGImages/'

mkdir(annotation_path)
mkdir(image_sets_path)
mkdir(jpeg_path)

dic = {}

for dirs in os.listdir(path):
    if os.path.isdir(dirs):
        if dirs != '' and dirs != 'output':
            # Annotations
            print('开始拷贝' + dirs + '的Annotation目录下的文件')
            p = os.path.join(path, dirs + '/Annotations')
            for file in os.listdir(p):
                print(file)
                file_back = os.path.join(path, dirs + '/Annotations/' + file)
                file_dest = os.path.join(path,  'output/Annotations/')
                shutil.copy(file_back, file_dest)

            # JPEGImages
            print('开始拷贝' + dirs + '的JPEGImages目录下的文件')
            p1 = os.path.join(path, dirs + '/JPEGImages')
            for file in os.listdir(p1):
                print(file)
                file_back = os.path.join(path, dirs + '/JPEGImages/' + file)
                file_dest = os.path.join(path,  'output/JPEGImages/')
                shutil.copy(file_back, file_dest)

            # Main
            print('开始合并' + dirs + '的Main目录下的文件')
            p2 = os.path.join(path, dirs + '/ImageSets/Main')

            for file in os.listdir(p2):
                # print('==' + file)
                file_location = os.path.join(path, dirs + '/ImageSets/Main/' + file)
                # print(file_location)

                if dic.__contains__(file):
                    dic[file].append(file_location)
                else:
                    dic[file] = []
                    dic[file].append(file_location)
print(dic)

# 合并文件
for key in dic:
    f = open(image_sets_path + '/' + key, 'w')
    for item in dic[key]:
        for line in open(item):
            f.writelines(line)
    f.close()
else:
    print('done!')