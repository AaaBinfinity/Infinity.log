from flask import Blueprint, jsonify
import json
import os
from pathlib import Path

quiz_bp = Blueprint('quiz', __name__, url_prefix='/api')

@quiz_bp.route('/quiz')
def get_quiz():
    try:
        # Using Path for more reliable path handling
        json_path = Path(__file__).parent / 'data' / 'quiz_data.json'
        
        # Verify file exists before opening
        if not json_path.exists():
            return jsonify({"error": "Quiz data file not found"}), 404
            
        # Open and read the JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            quiz_data = json.load(f)
            
        # Validate the loaded data structure
        if not isinstance(quiz_data, list):
            return jsonify({"error": "Invalid quiz data format - expected array"}), 500
            
        return jsonify({"data": quiz_data})
        
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500