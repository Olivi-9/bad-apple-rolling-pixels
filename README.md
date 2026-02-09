# Bad Apple Rolling Pixels

### 环境要求

```
Python 3.7+
opencv-python
numpy
numba
moviepy
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用方法

1. 将你的视频文件放在项目目录下
2. 修改 `main.py` 中的视频路径：
   ```python
   video = "你的视频文件.mp4"    # 输入视频路径
   videoout = "output.mp4"        # 输出视频路径
   ```
3. 运行程序：
   ```bash
   python main.py
   ```
4. 等待处理完成，将生成 `output.mp4` 和 `output.mp3`

### 参数调整

在 `change_img` 函数中可以调整滚动像素数量：
```python
former_img[i][pos[p]:pos[p+1]] = np.roll(former_img[i][pos[p]:pos[p+1]], 15*(1-2*int(flag)))
```
修改 `15` 这个值可以改变滚动强度。

在 `binarization` 函数中可以调整二值化阈值：
```python
ret, img_o = cv2.threshold(img_g, 150, 255, cv2.THRESH_BINARY)
```
修改 `150` 可以改变黑白区域的分界线。

### 项目结构

```
bad-apple-rolling-pixels/
├── main.py              # 主程序
├── requirements.txt     # 依赖列表
└── README.md           # 说明文档
```

### 工作原理

1. **初始化**：生成随机黑白噪声图像作为起始帧
2. **二值化**：将原视频每一帧转换为黑白图像
3. **区域检测**：检测每行的黑白边界
4. **像素滚动**：根据当前区域颜色，向左或向右滚动像素
5. **帧累积**：每一帧都基于上一帧的结果进行变换

### 性能说明

- 使用 Numba JIT 编译优化核心算法
- 处理时间取决于视频分辨率和长度
- 建议在处理高分辨率视频时保证足够的内存空间


