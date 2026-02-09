import time
import cv2
import numpy as np
import random
import numba
from moviepy import VideoFileClip

video = "Bad Apple but it's in 4k 60fps.mp4"    #在此处更改原影片的路径
videoout = "output.mp4"    #输出路径
capture = cv2.VideoCapture(video)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(capture.get(cv2.CAP_PROP_FPS))
height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
writer = cv2.VideoWriter(videoout, fourcc, fps, (width, height), True)

def creat_noise(height, width):
    img = np.zeros((height,width,3),dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            rand = random.randint(0,1) * 255
            for r in range(3):
                img[i][j][r] = rand
    return img

def binarization(img):
    # img = cv2.medianBlur(img,5)
    img_g = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,img_o = cv2.threshold(img_g, 150, 255, cv2.THRESH_BINARY)
    return img_o

# def get_edge(img):
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     canny = cv2.Canny(gray,100,200)
#     return canny

@numba.jit(nopython=True)
def change_img(gray_img,former_img):
    for i in range(height):
        pos = [0]
        flag = (gray_img[i][0] == 0)
        for j in range(width-1):
            if gray_img[i][j] != gray_img[i][j + 1]:
                pos.append(j + 1)
        pos.append(width-1)
        for p in range(len(pos)-1):
            former_img[i][pos[p]:pos[p+1]] = np.roll(former_img[i][pos[p]:pos[p+1]],15*(1-2*int(flag)))
            flag = not flag
    return former_img

def main():
    ind = 0
    former_img = creat_noise(height, width)
    while capture.isOpened():
        ret, img_src = capture.read()
        if not ret:
            print('end')
            break
        gray_img = binarization(img_src)
        img_out = change_img(gray_img,former_img)
        writer.write(img_out)
        former_img = img_out
        ind += 1
        print("{}/{}".format(ind,frame_count))
    writer.release()

vdu = VideoFileClip(video)
audio = vdu.audio
audio.write_audiofile("output.mp3")

s = time.time()
main()
e = time.time()
print("耗时{}秒".format(int(e-s)))
