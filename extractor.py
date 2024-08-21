import cv2
import os

# 동영상 파일 경로
video_name = 'F1.mp4'
input_fps = 30

video_path = './video/'

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path + video_name)


# 프레임 번호 초기화
frame_number = 0

video_fps = round(cap.get(cv2.CAP_PROP_FPS))

print('video fps :' , video_fps)

output_folder = 'workspace/' + video_name.split('.')[0] + '_' + str(input_fps) + 'fps/dataset'

# 저장할 이미지 경로
os.makedirs(output_folder, exist_ok=True)

# 동영상의 프레임을 하나씩 읽어서 이미지로 저장
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    if frame_number%(video_fps/input_fps) == 0:
        frame_filename = os.path.join(output_folder, f'frame_{frame_number}.png')
        # cv2.imwrite(frame_filename, frame[85:926, : ])
        cv2.imwrite(frame_filename, frame)
    
    frame_number += 1

# 캡처 객체 해제
cap.release()

print(f'Extracted {frame_number} frames to "{output_folder}"')
