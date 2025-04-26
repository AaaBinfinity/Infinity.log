from flask import Blueprint, jsonify
import json
import os
from pathlib import Path

quotes_bp = Blueprint('quotes', __name__, url_prefix='/api')

@quotes_bp.route('/quotes')
def get_quotes():
    try:
        # 使用 Path 构建文件路径
        json_path = Path(__file__).parent / 'data' / 'quotes_data.json'
        
        # 检查文件是否存在
        if not json_path.exists():
            return jsonify({"error": "Quotes data file not found"}), 404
            
        # 读取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            quotes_data = json.load(f)
            
        # 验证数据格式（应该是字符串数组）
        if not isinstance(quotes_data, list) or not all(isinstance(item, str) for item in quotes_data):
            return jsonify({"error": "Invalid quotes data format - expected array of strings"}), 500
            
        return jsonify({"data": quotes_data})
        
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500