from flask import Blueprint, jsonify
from ..services.qiniu_service import list_images

images_bp = Blueprint('images', __name__, url_prefix='/api')

@images_bp.route('/images', methods=['GET'])
def get_images():
    try:
        image_files = list_images()
        if not image_files:
            return jsonify(error='没有找到图片文件'), 404
        return jsonify(images=image_files)
    except Exception as e:
        print(f"获取图片文件失败: {str(e)}")
        return jsonify(error="服务器内部错误"), 500