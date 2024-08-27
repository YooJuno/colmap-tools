import struct

def read_binary(path):
    with open(path, "rb") as f:
        num_images = struct.unpack("<Q", f.read(8))[0]
        images = {}
        for _ in range(num_images):
            image_id = struct.unpack("<I", f.read(4))[0]
            qw, qx, qy, qz = struct.unpack("<dddd", f.read(8 * 4))
            tx, ty, tz = struct.unpack("<ddd", f.read(8 * 3))
            camera_id = struct.unpack("<I", f.read(4))[0]
            name = ""
            while True:
                c = f.read(1)
                if c == b"\x00":
                    break
                name += c.decode("utf-8")
            num_points2D = struct.unpack("<Q", f.read(8))[0]
            points2D = []
            for _ in range(num_points2D):
                x, y, point3D_id = struct.unpack("<ddq", f.read(8 * 2 + 8))
                points2D.append((x, y, point3D_id))
            images[image_id] = {
                "qw": qw, "qx": qx, "qy": qy, "qz": qz,
                "tx": tx, "ty": ty, "tz": tz,
                "camera_id": camera_id,
                "name": name,
                "points2D": points2D
            }
    return images

if __name__ == "__main__":
    images = read_binary('./workspaces/Sample_2_15fps/sparse/0/images.bin')

    for image_id, image_info in images.items():
        print(f"Name: {image_info['name']}")
        print(f"Translation: {image_info['tx'], image_info['ty'], image_info['tz']}")
        print()
