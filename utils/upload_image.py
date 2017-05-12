import uuid
import os
import platform


def save_image(img):
    if img:
        nid = str(uuid.uuid4())
        filename = img.name
        size = img.size
        name = nid + filename
        if platform.system() == 'Windows':
            file_path = os.path.join(r'static\upload\product_images', name)
        elif platform.system() == 'Linux':
            file_path = os.path.join(r'static/upload/product_images', name)

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
        sysattr = platform.system()
        if sysattr == 'Windows':
            base_dir = r'static\upload'
        elif sysattr == 'Linux':
            base_dir = r'static/upload'

        if type == 'article':
            file_path = os.path.join(base_dir, r'articles_images', file_name)
        elif type == 'product':
            file_path = os.path.join(base_dir, r'product_images', file_name)

        with open(file_path, 'wb') as f:
            for line in img.chunks():
                f.write(line)

        # res_dict['url'] = r'\{}'.format(file_path)

        if platform.system() == 'Windows':
            url = r'\{}'.format(file_path)
            url = url.replace('\\', '/')
            res_dict['url'] = url
        elif platform.system() == 'Linux':
            res_dict['url'] = r'/{}'.format(file_path)
        return res_dict
