import cv2
import os
import numpy as np

def make_masking_image_of(frame):
    roi_y = []
    cnt = 0

    def mouse_callback(event, x, y, flags, param):
        nonlocal cnt
        if event == cv2.EVENT_LBUTTONDOWN:
            roi_y.append(y)
            cnt += 1
    
    cv2.namedWindow('Set RoI Mask')
    cv2.setMouseCallback('Set RoI Mask', mouse_callback)

    while True:
        cv2.imshow('Set RoI Mask', frame)
        cv2.waitKey(1)
        if cnt == 2:
            break

    mask = np.zeros((frame.shape[0],frame.shape[1]), dtype=np.uint8)
    mask[min(roi_y):max(roi_y), : ] = 255 # RoI
    
    return mask


def extract_frames_from(video_path, video_name, output_fps):
    frame_number = 0
    first_frame = None
    output_folder_path = 'workspace/' + video_name.split('.')[0] + '_' + str(output_fps) + 'fps/dataset'

    os.makedirs(output_folder_path, exist_ok=True)

    cap = cv2.VideoCapture(video_path + video_name)
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_number%(round(cap.get(cv2.CAP_PROP_FPS))/output_fps) == 0:
            frame_filename = os.path.join(output_folder_path, f'frame_{frame_number}.png')
            cv2.imwrite(frame_filename, frame)
        
        if frame_number == 0:
            first_frame = frame.copy()
        frame_number += 1
    cap.release()
    
    print(f'Extracted {frame_number} frames to "{output_folder_path}"')
    
    return first_frame
        
        
if __name__ == '__main__':
    input_video_path = './video/'
    input_video_name = 'R1.mp4'
    output_fps = 1
    
    reference_frame = extract_frames_from(input_video_path, input_video_name, output_fps)
    
    mask_frame = make_masking_image_of(reference_frame)
    
    # output_folder_path = 'workspace/' + input_video_name.split('.')[0] + '_' + str(output_fps) + 'fps/mask'
    output_folder_path = f'workspace/{input_video_name.split('.')[0]}_{str(output_fps)}fps/mask'
    os.makedirs(output_folder_path, exist_ok=True)
    mask_filename = os.path.join(output_folder_path, f'{input_video_name.split('.')[0]}_mask.png')
    cv2.imwrite(mask_filename, mask_frame)
