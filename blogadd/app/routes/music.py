from flask import Blueprint, jsonify
import random
from ..services.qiniu_service import list_music_files

music_bp = Blueprint('music', __name__, url_prefix='/api')

@music_bp.route('/music', methods=['GET'])
def list_music():
    try:
        music_files = list_music_files()
        if not music_files:
            return jsonify(error='没有找到音乐文件'), 404
        selected = random.choice(music_files)
        return jsonify(music=selected)
    except Exception as e:
        print(f"获取音乐文件失败: {str(e)}")
        return jsonify(error="服务器内部错误"), 500