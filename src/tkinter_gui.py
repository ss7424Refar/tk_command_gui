from tkinter import *
from tkinter import messagebox as msg_box
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
import configparser
import subprocess
import threading
import json

class Base:
    def __init__(self, master):
        self.root = master
        self.root.config()
        self.root.title('Index Page')
        # 设置窗口大小
        self.width = 540
        self.height = 260

        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        align = '%dx%d+%d+%d' % (self.width, self.height, (screenwidth - self.width) / 2, (screenheight - self.height) / 2)
        self.root.geometry(align)

        # 设置窗口是否可变长
        self.root.resizable(width=False, height=False)

        Index(self.root)


class Index:
    def __init__(self, master):
        self.master = master
        self.faceIndex = Frame(self.master)
        self.faceIndex.config(bg='Ivory')
        self.faceIndex.place(x=0, y=0, width=540, height=290)
        Button(self.faceIndex, text='Convert To TF', command=self.convert).place(x=20, y=30, width=500, height=60)
        Button(self.faceIndex, text='Run Model', command=self.run).place(x=20, y=100, width=500, height=60)
        Button(self.faceIndex, text='Count Tag', command=self.count).place(x=20, y=170, width=500, height=60)


    def convert(self):
        self.faceIndex.destroy()
        Face1(self.master)

    def run(self):
        self.faceIndex.destroy()
        Face2(self.master)

    def count(self):
        self.faceIndex.destroy()
        Face3(self.master)


class Face1:
    def __init__(self, master):
        self.master = master
        self.face1 = Frame(self.master)
        self.face1.config(bg='Beige')
        self.face1.place(x=0, y=0, width=540, height=260)

        self.pb_path = StringVar()
        self.output_path = StringVar()

        cf = configparser.ConfigParser()
        cf.read(os.getcwd() + "/gui.ini")
        self.pb = cf.get("path", "pb")
        self.output = cf.get("path", "output")

        # pb path
        Label(self.face1, text="pb path").place(x=20, y=36, width=100, height=40)
        Entry(self.face1, textvariable=self.pb_path).place(x=123, y=36, width=270, height=40)
        Button(self.face1, text="add", command=self.add_pb_path).place(x=405, y=36, width=70, height=40)

        # output path
        Label(self.face1, text="output path").place(x=20, y=85, width=100, height=40)
        Entry(self.face1, textvariable=self.output_path).place(x=123, y=85, width=270, height=40)
        Button(self.face1, text="add", command=self.add_output_path).place(x=405, y=85, width=70, height=40)

        Button(self.face1, text="convert", bg="white", command=lambda: self.thread_it(self.on_convert)).place(x=20, y=150,
                                                                                                      width=140,
                                                                                                      height=40)

        Button(self.face1, text="back", bg="yellow", command=lambda: self.thread_it(self.back)).place(x=180, y=150,
                                                                                                      width=140,
                                                                                                      height=40)

    def add_pb_path(self):
        value = askdirectory(title='add_pb_path', initialdir=self.pb)
        self.pb_path.set(value)

    def add_output_path(self):
        value = askdirectory(title='add_output_path', initialdir=self.output)
        self.output_path.set(value)

    def on_convert(self):
        path1 = self.pb_path.get()
        path2 = self.output_path.get()
        if path1 == "":
            msg_box.showerror("Error", "please select pb path")
            return
        if path2 == "":
            msg_box.showerror("Error", "please select output path")
            return

        cmd = 'python ./mo_tf.py --input_model="' + path1 + '/frozen_inference_graph.pb"' + \
              ' --tensorflow_use_custom_operations_config extensions/front/tf/ssd_v2_support.json ' \
              '--tensorflow_object_detection_api_pipeline_config '\
              + path2 + 'pipeline.config --output="detection_boxes,detection_scores,num_detections" ' \
                        '--output_dir=' + path2 + ' --reverse_input_channels'

        print(cmd)
        p = subprocess.Popen("cmd.exe /c" + cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        curline = p.stdout.readline()
        while (curline != b''):
            print(curline.decode("gbk"))
            curline = p.stdout.readline()

        p.wait()
        print(p.returncode)

    def thread_it(self, func, *args):
        # 创建
        t = threading.Thread(target=func, args=args)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def back(self):
        self.face1.destroy()
        Index(self.master)


class Face2:
    def __init__(self, master):
        self.master = master
        self.face1 = Frame(self.master)
        self.face1.config(bg='Beige')
        self.face1.place(x=0, y=0, width=540, height=260)

        self.video_path = StringVar()
        self.model_path = StringVar()
        self.rate = StringVar()
        self.rate.set(0.8)

        cf = configparser.ConfigParser()
        cf.read(os.getcwd() + "/gui.ini")
        self.video = cf.get("path", "video")
        self.model = cf.get("path", "model")
        self.sdk = cf.get("path", "sdk")

        # video path
        Label(self.face1, text="video path").place(x=20, y=36, width=100, height=40)
        Entry(self.face1, textvariable=self.video_path).place(x=123, y=36, width=270, height=40)
        Button(self.face1, text="add", command=self.add_video_path).place(x=405, y=36, width=70, height=40)

        # model path
        Label(self.face1, text="model path").place(x=20, y=85, width=100, height=40)
        Entry(self.face1, textvariable=self.model_path).place(x=123, y=85, width=270, height=40)
        Button(self.face1, text="add", command=self.add_model_path).place(x=405, y=85, width=70, height=40)

        # value
        Label(self.face1, text="rate").place(x=20, y=130, width=100, height=40)
        Entry(self.face1, textvariable=self.rate).place(x=123, y=130, width=60, height=40)

        # Button(self.face1, text='back', command=self.back).place(x=123, y=100, width=60, height=40)

        Button(self.face1, text="run", bg="white", command=lambda: self.thread_it(self.on_run)).place(x=210, y=130,
                                                                                                      width=80,
                                                                                                      height=40)

        Button(self.face1, text="stop", bg="yellow", command=lambda: self.thread_it(self.on_stop)).place(x=300, y=130,
                                                                                                         width=80,
                                                                                                         height=40)

        Button(self.face1, text="back", bg="yellow", command=lambda: self.thread_it(self.back)).place(x=390, y=130,
                                                                                                      width=80,
                                                                                                      height=40)

    def add_video_path(self):
        value = askopenfilename(title='add_video_path', filetypes=[("videos", "*.mp4")], initialdir=self.video)
        self.video_path.set(value)

    def add_model_path(self):
        value = askopenfilename(title='add_model_path', filetypes=[("model", "*.xml")], initialdir=self.model)
        self.model_path.set(value)

    def on_run(self):
        path1 = self.video_path.get()
        path2 = self.model_path.get()
        if path1 == "":
            msg_box.showerror("Error", "please select video path")
            return
        if path2 == "":
            msg_box.showerror("Error", "please select model path")
            return

        d = os.path.dirname(__file__)  # 返回当前文件所在的目录
        parent_path = os.path.dirname(d)  # 获得d所在的目录,即d的父级目录
        parent_path = parent_path.replace('/', '\\')

        # 创建空文件
        batch_path = "./run.bat"
        fp = open(batch_path, 'w')
        fp.write('cd ' + self.sdk + '\n')
        fp.write('call setupvars.bat' + '\n')
        fp.write('cd ' + parent_path + '\\lib' + '\n')
        fp.write('object_detection_demo_ssd_async.exe -i ' + path1 + ' -m ' + path2 + ' -d CPU -t ' + self.rate.get() + '\n')
        fp.close()

        p = subprocess.Popen("cmd.exe /c" + "run.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def on_stop(self):
        cmd = "taskkill /F /IM object_detection_demo_ssd_async.exe"
        p = subprocess.Popen("cmd.exe /c" + cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        curline = p.stdout.readline()
        while (curline != b''):
            print(curline.decode("gbk"))
            curline = p.stdout.readline()

        p.wait()
        print(p.returncode)

    def thread_it(self, func, *args):
        # 创建
        t = threading.Thread(target=func, args=args)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()

    def back(self):
        self.face1.destroy()
        Index(self.master)


class Face3:
    def __init__(self, master):
        self.master = master
        self.face1 = Frame(self.master)
        self.face1.config(bg='Beige')
        self.face1.place(x=0, y=0, width=540, height=260)

        self.json_path = StringVar()

        cf = configparser.ConfigParser()
        cf.read(os.getcwd() + "/gui.ini")
        self.json = cf.get("path", "json")

        # json path
        Label(self.face1, text="json path").place(x=20, y=36, width=100, height=40)
        Entry(self.face1, textvariable=self.json_path).place(x=123, y=36, width=270, height=40)
        Button(self.face1, text="add", command=self.add_json_path).place(x=405, y=36, width=70, height=40)


        Button(self.face1, text="count", bg="white", command=self.on_count).place(x=20, y=100,width=140,height=40)

        Button(self.face1, text="back", bg="yellow", command=self.back).place(x=180, y=100,width=140,height=40)


    def add_json_path(self):
        value = askopenfilename(title='add_json_path', filetypes=[("json", "*.json")], initialdir=self.json)
        self.json_path.set(value)

    def on_count(self):
        path1 = self.json_path.get()
        if path1 == "":
            msg_box.showerror("Error", "please select json path")
            return
        f = open(path1, 'r')
        content = f.read()

        detail = json.loads(content)

        c = detail['frames']

        dic = {}
        for item in c:
            if len(c[item]):
                v = c[item]
                for index in range(len(v)):
                    s = v[index]
                    tag = s['tags'][0]
                    if dic.__contains__(tag):
                        dic[tag] = dic[tag] + 1
                    else:
                        dic[tag] = 1
        msg_box.showinfo("Info", dic)
        print(dic)

    def back(self):
        self.face1.destroy()
        Index(self.master)


if __name__ == '__main__':
    root = Tk()
    Base(root)
    root.mainloop()



