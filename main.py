import cv2
import numpy as np
from pywinauto import Application
import pygetwindow as gw
import os
import yaml

with open("config.yaml", 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

target_window_title = config['window_title']  # 从配置中获取目标窗口标题
autopause = config['autopause']  # 从配置中获取是否自动暂停
video_width = config['video_resolution']['width']  # 从配置中获取视频分辨率宽
video_height = config['video_resolution']['height']  # 从配置中获取视频分辨率长
FRAME_INTERVAL = config['detection_interval']  # 从配置中获取检测间隔

def zhixing(titlename):  # 定义执行行为
    print(F"执行预设操作：切换至 {target_window_title}")
    app = Application().connect(title=titlename)
    window = app.window(title=titlename)
    if window.is_minimized():
        window.restore()
    window.set_focus()
    if autopause:
        os.system('pause')

net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "deploy.caffemodel")
windows = gw.getAllTitles()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)  # 视频分辨率 长
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)  # 视频分辨率 宽
CLASSES = {15: "person"}

once = False
frame_count = 0
prev_person_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1
    if frame_count % FRAME_INTERVAL == 0:
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()
        person_count = 0
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            class_id = int(detections[0, 0, i, 1])
            if confidence > 0.5 and class_id in CLASSES:
                person_count += 1
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(frame, f"Person: {confidence:.2f}", (startX, startY - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if person_count > prev_person_count and once:
            print("检测到新的人进入")
            zhixing(target_window_title)
        elif not once:
            print("获取主人物成功")
            once = True
        prev_person_count = person_count
    cv2.imshow("Person Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
