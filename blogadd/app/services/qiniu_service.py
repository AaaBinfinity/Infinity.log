from qiniu import Auth, BucketManager
from ..config import Config

def list_images():
    """列出七牛云中的图片文件"""
    q = Auth(Config.QINIU_ACCESS_KEY, Config.QINIU_SECRET_KEY)
    bucket = BucketManager(q)

    prefix = 'aboutimgs/'
    limit = 100
    marker = None
    image_files = []

    while True:
        ret, eof, info = bucket.list(Config.QINIU_BUCKET_NAME, prefix=prefix, marker=marker, limit=limit)
        if info.status_code != 200 or not ret or 'items' not in ret:
            raise Exception('获取图片列表失败')

        for item in ret['items']:
            key = item['key']
            if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_files.append({
                    'src': f"{Config.QINIU_DOMAIN}/{key}"
                })

        if eof:
            break
        marker = ret.get('marker')

    return image_files

def list_music_files():
    """列出七牛云中的音乐文件"""
    q = Auth(Config.QINIU_ACCESS_KEY, Config.QINIU_SECRET_KEY)
    bucket = BucketManager(q)

    limit = 100
    marker = None
    music_files = []

    while True:
        ret, eof, info = bucket.list(Config.QINIU_BUCKET_NAME, prefix='', marker=marker, limit=limit)
        if info.status_code != 200 or not ret or 'items' not in ret:
            raise Exception('获取音乐列表失败')

        for item in ret['items']:
            key = item['key']
            if key.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                music_files.append({
                    'name': key,
                    'url': f"{Config.QINIU_DOMAIN}/{key}"
                })

        if eof:
            break
        marker = ret.get('marker')

    return music_files