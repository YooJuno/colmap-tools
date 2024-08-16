import cv2
import os

# 동영상 파일 경로
video_path = 'IMG_5606.MOV'

# 저장할 이미지 경로
output_folder = 'frames'
os.makedirs(output_folder, exist_ok=True)

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(video_path)

# 프레임 번호 초기화
frame_number = 0

# 동영상의 프레임을 하나씩 읽어서 이미지로 저장
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 프레임 저장 (예: frame_0.png, frame_1.png, ...)
    frame_filename = os.path.join(output_folder, f'frame_{frame_number}.png')
    cv2.imwrite(frame_filename, frame)
    
    frame_number += 1

# 캡처 객체 해제
cap.release()

print(f'Extracted {frame_number} frames to "{output_folder}"')
