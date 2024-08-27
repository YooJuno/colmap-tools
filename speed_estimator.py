import math
import yaml
from binary_reader import read_binary
import cv2

def calc_dist(src, dst):
    return math.sqrt(math.pow(src[0]-dst[0],2) + math.pow(src[1]-dst[1],2) + math.pow(src[2]-dst[2],2))

if __name__ == '__main__':
    # yaml_name = 'F1.yaml' 
    # yaml_name = 'R1.yaml'
    # yaml_name = 'Sample_1.yaml'
    # yaml_name = 'Sample_2.yaml'
    yaml_name = 'Sample_3.yaml'
    
    with open(yaml_name, 'r') as file:
        data = yaml.safe_load(file)
    fps = data['fps']
    
    video_path = data['video_path']
    binary_path = data['binary_path']
    real_reference_distance_meter = data['real_reference_distance_meter']
    virtual_reference_positions_pixel = data['virtual_reference_positions_pixel']
    
    camera_positions_pixel = []
    
    images_info_list = read_binary(binary_path)
    
    for _, image_info in images_info_list.items():
        # (index, [tx, ty, tz])
        camera_positions_pixel.append((int(image_info['name'].split('.')[0].split('_')[-1]), [image_info['tx'], image_info['ty'], image_info['tz']]))
    
    # sorted by index
    camera_positions_pixel = sorted(camera_positions_pixel, key=lambda x: x[0])
    for info in camera_positions_pixel:
        print (info)

    virtual_reference_distance_pixel = 0
    for i in range(len(virtual_reference_positions_pixel)-1):
        virtual_reference_distance_pixel += calc_dist(virtual_reference_positions_pixel[i], virtual_reference_positions_pixel[i+1])
    
    ratio_meter_to_pixel = real_reference_distance_meter / virtual_reference_distance_pixel
    print("ratio : %5.2f[m/pxls]"%(ratio_meter_to_pixel))

    frame_interval = 1
    estimated_speed_km_h = []
    for i in range(0, len(camera_positions_pixel)- frame_interval, frame_interval):
        duration_hours = ((camera_positions_pixel[i+frame_interval][0] - camera_positions_pixel[i][0])/fps) / (60 * 60)
        speed_index = camera_positions_pixel[i+frame_interval][0]
        speed_value = (calc_dist(camera_positions_pixel[i+frame_interval][1], camera_positions_pixel[i][1]) * ratio_meter_to_pixel) / 1000 / duration_hours
        estimated_speed_km_h.append((speed_index, speed_value))
    
    cap = cv2.VideoCapture(video_path)
    frame_index = 0
    speed_iter = 0
    font_scale = 0.5
    text = "[...km/h]"
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (frame.shape[1]//2, frame.shape[0]//2))
        if not ret:
            break
        
        if frame_index == estimated_speed_km_h[speed_iter][0]:
            text = '[%3d km/h]'%(estimated_speed_km_h[speed_iter][1])
            speed_iter += 1
        cv2.putText(frame, text, (frame.shape[1]//2+60, 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 2)
        
        cv2.imshow("Speed Estimation", frame)
        
        if cv2.waitKey(0) == 27:
            break
        
        frame_index += 1
