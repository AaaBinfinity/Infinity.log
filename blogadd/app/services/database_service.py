import pymysql
from ..config import Config

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(**Config.DB_CONFIG)