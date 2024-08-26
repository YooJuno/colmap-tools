import math
import yaml

def calc_dist(src, dst):
    return math.sqrt(math.pow(src[0]-dst[0],2) + math.pow(src[1]-dst[1],2) + math.pow(src[2]-dst[2],2))

if __name__ == '__main__':
    with open('R1.yaml', 'r') as file:
        data = yaml.safe_load(file)
    
    fps = data['fps']
    camera_positions_pixel = data['camera_positions_pixel']
    real_distance_meter = data['real_distance_meter']
    frame_indexes = data['frame_indexes']
    real_speed_km_h = data['real_speed']
    
    virtual_reference_positions_pixel = data['virtual_reference_positions_pixel']
    virtual_reference_distance_pixel = 0
    
    for i in range(len(virtual_reference_positions_pixel)-1):
        virtual_reference_distance_pixel += calc_dist(virtual_reference_positions_pixel[i], virtual_reference_positions_pixel[i+1])
    
    ratio_meter_to_pixel = real_distance_meter / virtual_reference_distance_pixel
    print("ratio : %5.2f[m/pxls]"%(ratio_meter_to_pixel))

    for i in range(len(frame_indexes)-1):
        duration_h = ((frame_indexes[i+1] - frame_indexes[i])/fps) / (60 * 60)
        estimated_speed_km_h = (calc_dist(camera_positions_pixel[i+1], camera_positions_pixel[i]) * ratio_meter_to_pixel / 1000) / duration_h
        print("%3d) Estimation: %4.1f[km/h]"%(frame_indexes[i+1], estimated_speed_km_h), end='')
        print(f",  GPS:% 3d[km/h]"%(real_speed_km_h[i]))
