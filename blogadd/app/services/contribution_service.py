from datetime import datetime, timedelta
import calendar
from ..config import Config
from .database_service import get_db_connection

def get_contributions():
    """获取近30天每日文章贡献量"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 计算时间范围（包含当天）
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')

            sql = """
                SELECT 
                    DATE(create_time) AS day,
                    COUNT(*) AS count
                FROM sys_article
                WHERE create_time >= %s
                GROUP BY day
                ORDER BY day
            """
            cursor.execute(sql, (start_date,))
            db_results = cursor.fetchall()
            
            result_dict = {row[0].strftime('%Y-%m-%d'): row[1] for row in db_results}

            date_list = [(datetime.now() - timedelta(days=i)).date() 
                       for i in range(29, -1, -1)]

            formatted_data = []
            for date in date_list:
                date_str = date.strftime('%Y-%m-%d')
                formatted_data.append({
                    "day": date_str[5:],  # 返回MM-DD格式
                    "count": result_dict.get(date_str, 0)
                })

            return formatted_data
    except Exception as e:
        print(f"数据库查询失败: {str(e)}")
        return []
    finally:
        connection.close()

def get_yearly_contributions():
    """获取本年每日文章贡献量"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            start_date = datetime(datetime.now().year, 1, 1)
            end_date = datetime(datetime.now().year, 12, 31)

            sql = """
                SELECT 
                    DATE(create_time) AS day,
                    COUNT(*) AS count
                FROM sys_article
                WHERE create_time >= %s AND create_time <= %s
                GROUP BY day
                ORDER BY day
            """
            cursor.execute(sql, (start_date, end_date))
            db_results = cursor.fetchall()
            
            result_dict = {row[0].strftime('%Y-%m-%d'): row[1] for row in db_results}

            date_list = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

            formatted_data = []
            for date in date_list:
                date_str = date.strftime('%Y年%m月%d日')
                weekday = calendar.day_name[date.weekday()]
                formatted_data.append({
                    "date": date_str,
                    "weekday": weekday,
                    "count": result_dict.get(date.strftime('%Y-%m-%d'), 0)
                })

            return formatted_data
    except Exception as e:
        print(f"数据库查询失败: {str(e)}")
        return []
    finally:
        connection.close()