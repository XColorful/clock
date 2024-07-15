import tkinter as tk
import time
from math import radians, sin, cos
from PIL import Image, ImageTk
import os

# 更改工作路径为代码所在路径
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_config_dir():
    try:
        with open('config_dir.txt', 'r') as file:
            dir_path = file.readline().strip()
        if os.path.isdir(dir_path):
            return dir_path
        else:
            return os.getcwd()
    except FileNotFoundError:
        return os.getcwd()

# 读取配置文件
config = {}
config_dir = get_config_dir()
with open(os.path.join(config_dir, "config.txt"), 'r') as f:
    for line in f:
        key, value = line.strip().split(' = ')
        config[key] = value

# 将配置存储在变量中
hour_hand_length = int(config['hour_hand_length'])
hour_hand_color = config['hour_hand_color']
minute_hand_length = int(config['minute_hand_length'])
minute_hand_color = config['minute_hand_color']
second_hand_length = int(config['second_hand_length'])
second_hand_color = config['second_hand_color']
time_color = config['time_color']
time_bg_color = config['time_bg_color']
clock_dir = config["clock_dir"]

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Clock')
        self.geometry('300x300')
        self.attributes('-topmost', True)  # 窗口始终保持在最前面
        self.configure(bg='white')

        # 加载背景图片
        bg_image = Image.open(clock_dir)  # 将"background.jpg"替换为你的图片文件名
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # 创建画布并添加背景图片
        self.canvas = tk.Canvas(self, width=300, height=300, bg='#2b2b2b', bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # 创建显示时间的标签
        self.time_label = tk.Label(self, font=('Helvetica', 20), bg=time_bg_color, fg=time_color)
        self.time_label.place(x=150, y=250, anchor='center')

        # 更新时间
        self.update_time()

    def update_time(self):
        current_time = time.localtime()
        hours = current_time.tm_hour
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        # 计算时针、分针和秒针的角度
        hour_angle = radians((hours % 12 + minutes / 60) * 30 - 90)  # 这里考虑了分钟数
        minute_angle = radians(minutes * 6 - 90)
        second_angle = radians(seconds * 6 - 90)

        # 计算时针、分针和秒针的坐标
        hour_x = 150 + hour_hand_length * cos(hour_angle)
        hour_y = 150 + hour_hand_length * sin(hour_angle)
        minute_x = 150 + minute_hand_length * cos(minute_angle)
        minute_y = 150 + minute_hand_length * sin(minute_angle)
        second_x = 150 + second_hand_length * cos(second_angle)
        second_y = 150 + second_hand_length * sin(second_angle)

        # 删除旧的时针、分针和秒针
        self.canvas.delete('clock')

        # 画时针
        self.canvas.create_line(150, 150, hour_x, hour_y, fill=hour_hand_color, width=4, tags='clock')

        # 画分针
        self.canvas.create_line(150, 150, minute_x, minute_y, fill=minute_hand_color, width=2, tags='clock')

        # 画秒针
        self.canvas.create_line(150, 150, second_x, second_y, fill=second_hand_color, width=1, tags='clock')

        # 更新数字时间
        self.time_label.config(text=time.strftime('%H:%M:%S'))

        self.after(1000, self.update_time)  # 每1000毫秒（即1秒）更新一次时间

if __name__ == "__main__":
    clock = Clock()
    clock.mainloop()
