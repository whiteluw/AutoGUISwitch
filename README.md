# AutoGUISwitch
基于Python的OpenCV库实现调用摄像头来判断是否有第二个人，若有则执行自动切换到目标窗口。  
## 使用方法
1. 首先，运行get_title.ext，这会列出所有当前打开的窗口名  
2. 找到你要在摄像头检测到人后自动切换的窗口名，将其复制  
3. 打开config.yaml，修改window_title:参数  
4. 按需要调整性能设置，视频分辨率调高有助于提高检测速度，但同时会降低性能（占用更多CPU），检测间隔同理  

**config.yaml**
```yaml
# 功能设置：
  # 目标窗口标题
  window_title: ""

  # 是否在触发后自动暂停程序
  autopause: false

# 性能设置：
# 更快的检测速度意味着更差的性能
  # 视频分辨率设置
  video_resolution:
    # 视频宽度
    width: 640
    # 视频高度
    height: 480

  # 检测间隔，单位为帧，越低越快
  detection_interval: 5
```

## 开发
函数`zhixing()`用于存放检测到后的执行行为。
我们在发行版中默认提供了MobileNet-SSD-RealSense下的caffemodel/MobileNetSSD/MobileNetSSD_deploy.prototxt及caffemodel/MobileNetSSD/MobileNetSSD_deploy.caffemodel作为深度学习框架中的模型参数。
https://github.com/PINTO0309/MobileNet-SSD-RealSense