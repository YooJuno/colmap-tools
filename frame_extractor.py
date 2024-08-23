import cv2
import os
import numpy as np


def make_masking_image_of(origin):
    roi = []
    cnt = 0
    
    sketchbook_checkpoint = cv2.resize(origin, (origin.shape[1]//2, origin.shape[0]//2))
    sketchbook = sketchbook_checkpoint.copy()
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal cnt, sketchbook
        sketchbook = sketchbook_checkpoint.copy()
        sketchbook_height, sketchbook_width = sketchbook.shape[:2]
        
        text = f'[{x}, {y}]'
        text_width, text_height= cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        
        offset_y = 30
        text_tl_x = max(0, min(x - text_width//2, sketchbook_width - text_width))
        text_tl_y = min(sketchbook_height - text_height, y+offset_y)
        
        cv2.putText(sketchbook, f"[{x}, {y}]", (text_tl_x, text_tl_y), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(255, 255, 255), thickness=2)
        
        if cnt > 0:
            cv2.line(sketchbook, roi[cnt-1], (x, y), (0, 255, 0), thickness=2)
            
        if event == cv2.EVENT_LBUTTONDOWN:
            roi.append((x,y))
            cv2.circle(sketchbook_checkpoint, (x,y), 3, (0, 255, 0), thickness=3)
            if cnt > 0:
                cv2.line(sketchbook_checkpoint, roi[cnt-1], (x, y), (0, 255, 0), thickness=2)
            cnt += 1
    
    cv2.namedWindow('Set RoI Mask')
    cv2.setMouseCallback('Set RoI Mask', mouse_callback)

    while cnt < 4:
        cv2.imshow('Set RoI Mask', sketchbook)
        if cv2.waitKey(1) == 27:
            break
        
    cv2.destroyAllWindows()
    
    mask = np.zeros((origin.shape[0],origin.shape[1]), dtype=np.uint8)
    cv2.fillPoly(mask, [np.array(roi)* 2], color=(255, 255, 255))
    
    return mask


def extract_frames_from(video_path, video_name, output_fps):
    frame_number = 0
    
    output_folder_path = 'workspaces/' + video_name.split('.')[0] + '_' + str(output_fps) + 'fps/dataset'
    os.makedirs(output_folder_path, exist_ok=True)

    mask_folder_path = f'workspaces/{input_video_name.split(".")[0]}_{str(output_fps)}fps/mask'
    os.makedirs(mask_folder_path, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path + video_name)
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_number%(round(cap.get(cv2.CAP_PROP_FPS))/output_fps) == 0:
            frame_filename = os.path.join(output_folder_path, f'frame_{frame_number}.png')
            cv2.imwrite(frame_filename, frame)
        
            if frame_number == 0:
                mask_frame = make_masking_image_of(frame)
            mask_filename = os.path.join(mask_folder_path, f'frame_{frame_number}.png.png')
            cv2.imwrite(mask_filename, mask_frame)
        
        frame_number += 1
    cap.release()
    
    print(f'Extracted {frame_number} frames to "{output_folder_path}"')      
        
if __name__ == '__main__':
    input_video_path = './video/'
    input_video_name = 'Sample_2.mp4'
    output_fps = 10
    
    extract_frames_from(input_video_path, input_video_name, output_fps)
