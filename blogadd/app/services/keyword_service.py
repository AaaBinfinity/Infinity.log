from collections import Counter
from ..config import Config
from .database_service import get_db_connection
from ..utils.color_utils import get_color

def get_keywords():
    """获取关键词及其频率"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT keywords FROM sys_article"
            cursor.execute(sql)
            rows = cursor.fetchall()
            keywords = []
            for row in rows:
                keywords.extend(row[0].split(','))
            
            keyword_counts = Counter(keywords)
            max_frequency = max(keyword_counts.values(), default=1)

            result = [{'keyword': keyword, 'frequency': count, 'color': get_color(count, max_frequency)} 
                      for keyword, count in keyword_counts.items()]
            return result
    finally:
        connection.close()