import uuid
import os


def save_image(img):
    if img:
        nid = str(uuid.uuid4())
        filename = img.name
        size = img.size
        name = nid + filename
        file_path = os.path.join(r'static\upload\product_images', name)
        with open(file_path, 'wb') as f:
            for line in img.chunks():
                f.write(line)

        data = {}
        data['ul_name'] = name
        data['ul_sourcename'] = img.name
        data['ul_size'] = size
        data['ul_url'] = file_path
        return data
