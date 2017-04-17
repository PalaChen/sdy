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


def ckedit_upload_image(req, type):
    res_dict = {'error': 0, 'url': None, 'message': '图片上传成功'}
    if req.method == 'POST':
        img = req.FILES.get('imgFile')
        file_name = str(uuid.uuid4()) + img.name
        if type == 'article':
            file_path = os.path.join(r'static\upload\articles_image', file_name)
        elif type == 'product':
            file_path = os.path.join(r'static\upload\product_image', file_name)

        with open(file_path, 'wb') as f:
            for line in img.chunks():
                f.write(line)
        res_dict['url'] = r'\{}'.format(file_path)
        print(r'\{}'.format(file_path))
        return res_dict
