
from flask import Blueprint, jsonify
from ..services.contribution_service import get_contributions, get_yearly_contributions

contributions_bp = Blueprint('contributions', __name__, url_prefix='/api')

@contributions_bp.route('/contributions', methods=['GET'])
def contributions():
    try:
        contribution_data = get_contributions()
        return jsonify(contributions=contribution_data)
    except Exception as e:
        print(f"获取贡献数据失败: {str(e)}")
        return jsonify(error="服务器内部错误"), 500

@contributions_bp.route('/yearly_contributions', methods=['GET'])
def yearly_contributions():
    try:
        contribution_data = get_yearly_contributions()
        return jsonify(contributions=contribution_data)
    except Exception as e:
        print(f"获取年度贡献数据失败: {str(e)}")
        return jsonify(error="服务器内部错误"), 500