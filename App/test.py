#!/usr/bin/python3

import cv2
import pytube
reader = cv2.VideoCapture("static/video.mp4")
fps = reader.get(cv2.CAP_PROP_FPS)
print(fps)
num_frames = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
print(num_frames)

yt = pytube.YouTube("https://www.youtube.com/watch?v=GTh2tRAE2w4")
stream = yt.streams.first()

a = stream.download('static')
print("path", a)
