import cv2
import os
import numpy as np


video_name = 'F1.mp4'
input_fps = 30

video_path = './video/'

cap = cv2.VideoCapture(video_path + video_name)

frame_number = 0

video_fps = round(cap.get(cv2.CAP_PROP_FPS))
video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print('video fps :' , video_fps)

output_folder = 'workspace/' + video_name.split('.')[0] + '_' + str(input_fps) + 'fps/dataset'

os.makedirs(output_folder, exist_ok=True)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    if frame_number%(video_fps/input_fps) == 0:
        frame_filename = os.path.join(output_folder, f'frame_{frame_number}.png')
        cv2.imwrite(frame_filename, frame)
    
    frame_number += 1
    
cap.release()

mask = np.zeros((video_height,video_width), dtype=np.uint8)
mask[93:950, : ] = 255 # RoI

cv2.imwrite(video_name.split('.')[0] + '_mask.png', mask)

print(f'Extracted {frame_number} frames to "{output_folder}"')
