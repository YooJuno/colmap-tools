import cv2
import os
import numpy as np


video_name = 'R1.mp4'
input_fps = 10

video_path = './video/'

cap = cv2.VideoCapture(video_path + video_name)

frame_number = 0

video_fps = round(cap.get(cv2.CAP_PROP_FPS))
video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print('video fps :' , video_fps)
output_folder = 'workspace/' + video_name.split('.')[0] + '_' + str(input_fps) + 'fps/dataset'
os.makedirs(output_folder, exist_ok=True)

frame_mask = 0

while True:
    ret, frame = cap.read()
    
    if frame_number == 0:
        frame_mask = frame.copy()
    
    if not ret:
        break
    
    if frame_number%(video_fps/input_fps) == 0:
        frame_filename = os.path.join(output_folder, f'frame_{frame_number}.png')
        cv2.imwrite(frame_filename, frame)
    
    frame_number += 1
    
cap.release()



pos_roi_y = []
cnt = 0

def mouse_callback(event, x, y, flags, param):
    global cnt
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 마우스 버튼 클릭 시
        pos_roi_y.append(y)
        cnt += 1
        print('hi')

cv2.namedWindow('Set RoI Mask')
cv2.setMouseCallback('Set RoI Mask', mouse_callback)

while True:
    cv2.imshow('Set RoI Mask', frame_mask)
    cv2.waitKey(1)
    # ESC 키를 누르면 종료
    if cnt == 2:
        break

mask = np.zeros((int(video_height),int(video_width)), dtype=np.uint8)
mask[min(pos_roi_y):max(pos_roi_y), : ] = 255 # RoI

output_folder = 'workspace/' + video_name.split('.')[0] + '_' + str(input_fps) + 'fps/mask'
os.makedirs(output_folder, exist_ok=True)
mask_filename = os.path.join(output_folder, '%s_mask.png'%(video_name.split('.')[0]))
cv2.imwrite(mask_filename, mask)

print(f'Extracted {frame_number} frames to "{output_folder}"')
