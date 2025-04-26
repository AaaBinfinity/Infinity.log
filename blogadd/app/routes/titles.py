from flask import Blueprint, jsonify
import json
from pathlib import Path

titles_bp = Blueprint('titles', __name__, url_prefix='/api')

@titles_bp.route('/titles')
def get_titles():
    try:
        # 构建 JSON 文件路径
        json_path = Path(__file__).parent / 'data' / 'titles_data.json'
        
        # 检查文件是否存在
        if not json_path.exists():
            return jsonify({"error": "Titles data file not found"}), 404
            
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            titles_data = json.load(f)
            
        # 验证数据格式（应为字符串数组）
        if not isinstance(titles_data, list) or not all(isinstance(item, str) for item in titles_data):
            return jsonify({"error": "Invalid titles data format - expected array of strings"}), 500
            
        return jsonify({"data": titles_data})
        
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500