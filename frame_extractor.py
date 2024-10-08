import cv2
import os
import numpy as np


def make_masking_image_of(origin):
    roi = []
    cnt = 0
    
    sketchbook_checkpoint = cv2.resize(origin, (origin.shape[1]//2, origin.shape[0]//2))
    sketchbook = sketchbook_checkpoint.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    def mouse_callback(event, x, y, flags, param):
        nonlocal cnt, sketchbook
        sketchbook = sketchbook_checkpoint.copy()
        sketchbook_height, sketchbook_width = sketchbook.shape[:2]
        
        text = f'[{x}, {y}]'
        font_scale = 0.5
        text_width, text_height= cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)[0]
        
        offset_y = 30
        text_tl_x = max(min(x - text_width//2, sketchbook_width - text_width), 0)
        text_tl_y = min(y+offset_y, sketchbook_height - text_height)
        
        cv2.putText(sketchbook, text, (text_tl_x, text_tl_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 2)
        
        if cnt > 0:
            cv2.line(sketchbook, roi[cnt-1], (x, y), (0, 255, 0), thickness=2)
            
        if event == cv2.EVENT_LBUTTONDOWN:
            roi.append((x,y))
            cv2.circle(sketchbook_checkpoint, (x,y), 3, (0, 255, 0), thickness=3)
            cv2.putText(sketchbook_checkpoint, f"[{x}, {y}]", (text_tl_x, text_tl_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color=(240, 255, 240), thickness=2)
            if cnt > 0:
                cv2.line(sketchbook_checkpoint, roi[cnt-1], (x, y), (0, 255, 0), thickness=2)
            cnt += 1
    
    cv2.namedWindow('Set RoI Mask')
    cv2.setMouseCallback('Set RoI Mask', mouse_callback)

    while cv2.waitKey(1) != 27:
        cv2.imshow('Set RoI Mask', sketchbook)
        
    cv2.destroyAllWindows()
    
    mask = np.zeros((origin.shape[0],origin.shape[1]), dtype=np.uint8)
    cv2.fillPoly(mask, [np.array(roi)* 2], color=(255, 255, 255))
    
    return mask


def Run(video_path, output_fps):
    frame_number = 0
    workspace_path = f'workspaces/{video_path.split("/")[-1].split(".")[0]}_{str(output_fps)}fps/'
    
    output_image_path = workspace_path + 'image'
    os.makedirs(output_image_path, exist_ok=True)

    mask_path = workspace_path + 'mask'
    os.makedirs(mask_path, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        if frame_number == 0:
            mask_frame = make_masking_image_of(frame)
            
        if frame_number%(round(cap.get(cv2.CAP_PROP_FPS))/output_fps) == 0:
            frame_filename = os.path.join(output_image_path, f'frame_{frame_number}.png')
            cv2.imwrite(frame_filename, frame)
        
            mask_filename = os.path.join(mask_path, f'frame_{frame_number}.png.png')
            cv2.imwrite(mask_filename, mask_frame)
        
        frame_number += 1
    cap.release()
    
    print('Extraction Complete!')


if __name__ == '__main__':
    input_video_path = './video/Sample_3.mp4'
    output_fps = 15
    
    Run(input_video_path, output_fps)
