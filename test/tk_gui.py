from tkinter import *

from tkinter import messagebox as msg_box
from tkinter.filedialog import askopenfilename
import os
import configparser
import subprocess
import threading

# 初始化Tk
window = Tk()
window.title('tk_command_gui')

# 设置窗口大小
width = 540
height = 500

# 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
align = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
window.geometry(align)

# 设置窗口是否可变长
window.resizable(width=False, height=False)


video_path = StringVar()
model_path = StringVar()
rate = StringVar()
rate.set(0.8)

cf = configparser.ConfigParser()


def add_video_path():
    cf.read("gui.ini")
    value = askopenfilename(title='add_video_path', filetypes=[("videos", "*.mp4")], initialdir=cf.get("path", "video"))
    video_path.set(value)


def add_model_path():
    cf.read("gui.ini")
    value = askopenfilename(title='add_model_path', filetypes=[("model", "*.xml")],  initialdir=cf.get("path", "model"))
    model_path.set(value)


# video path
Label(window, text="video path").place(x=20, y=36, width=100, height=40)
Entry(window, textvariable=video_path).place(x=123, y=36, width=270, height=40)
Button(window, text="add", command=add_video_path).place(x=405, y=36, width=70, height=40)

# model path
Label(window, text="model path").place(x=20, y=85, width=100, height=40)
Entry(window, textvariable=model_path).place(x=123, y=85, width=270, height=40)
Button(window, text="add", command=add_model_path).place(x=405, y=85, width=70, height=40)

# value
Label(window, text="rate").place(x=20, y=125, width=100, height=40)
Entry(window, textvariable=rate).place(x=123, y=130, width=60, height=40)


def on_run():
    path1 = video_path.get()
    path2 = model_path.get()
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
    cf.read("gui.ini")
    fp = open(batch_path, 'w')
    fp.write('cd ' + cf.get("path", "sdk") + '\n')
    fp.write('call setupvars.bat' + '\n')
    fp.write('cd ' + parent_path + '\\lib' + '\n')
    fp.write('object_detection_demo_ssd_async.exe -i ' + path1 + ' -m ' + path2 + ' -d CPU -t ' + rate.get() + '\n')
    fp.close()

    p = subprocess.Popen("cmd.exe /c" + "run.bat", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def on_stop():
    cmd = "taskkill /F /IM object_detection_demo_ssd_async.exe"
    p = subprocess.Popen("cmd.exe /c" + cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    curline = p.stdout.readline()
    while(curline != b''):
        # unicode_text = u"".join(curline)
        print(curline.decode("gbk"))
        curline = p.stdout.readline()

    p.wait()
    print(p.returncode)


def thread_it(func, *args):
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


Button(window, text="run", bg="white", command=lambda: thread_it(on_run)).place(x=260, y=130, width=100, height=40)

Button(window, text="stop", bg="yellow", command=lambda: thread_it(on_stop)).place(x=370, y=130, width=100, height=40)


Button(window, bg="black").place(x=0, y=190, width=550, height=3)





# 进入消息循环
window.mainloop()
