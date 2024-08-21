import cv2
import numpy as np

# 마우스 클릭 이벤트를 처리하는 함수 정의
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 마우스 버튼 클릭 시
        print(f"마우스 위치: x={x}, y={y}")

# 빈 이미지 생성 (예: 500x500 크기, 흰색)
image = cv2.imread("./workspace/F1_5fps/dataset/frame_0.png")

# 윈도우 생성 및 마우스 콜백 함수 등록
cv2.namedWindow('Mouse Event')
cv2.setMouseCallback('Mouse Event', mouse_callback)

print('height :', image.shape[0], 'width :', image.shape[1])

while True:
    # 이미지를 윈도우에 표시
    cv2.imshow('Mouse Event', image)
    
    # ESC 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 모든 윈도우 종료
cv2.destroyAllWindows()
