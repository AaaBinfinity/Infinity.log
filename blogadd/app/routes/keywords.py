from flask import Blueprint, jsonify
from ..services.keyword_service import get_keywords

keywords_bp = Blueprint('keywords', __name__, url_prefix='/api')

@keywords_bp.route('/keywords', methods=['GET'])
def keywords():
    keywords_data = get_keywords()
    return jsonify(keywords=keywords_data)