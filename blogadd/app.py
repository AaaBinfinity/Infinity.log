from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
from collections import Counter
from qiniu import Auth, BucketManager

# 七牛云配置
access_key = 'G4jrithVlVa8sw-gQ2wdb9eXmR-WbWjYzwvaSOKg'
secret_key = 'mnZgQQudQeAazpMhw_kEvGus7FWZ3LdXrS-Z-2R6'
bucket_name = 'infinitylogtemp'
domain = 'http://suwcoa2z3.hb-bkt.clouddn.com'  
# 创建 Flask 实例
app = Flask(__name__)

# 配置数据库连接
db_config = {
    'host': '1.92.109.205',
    'user': 'binfinity',
    'password': 'Cb050328_password',
    'database': 'InfinityLogDB',
    'charset': 'utf8mb4'
}

# 允许所有来源的请求
CORS(app)

def get_keywords():
    # 连接到数据库
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT keywords FROM sys_article"
            cursor.execute(sql)
            rows = cursor.fetchall()
            keywords = []
            for row in rows:
                # 将逗号分隔的关键词加入到列表中
                keywords.extend(row[0].split(','))
            
            # 使用 Counter 统计关键词频率
            keyword_counts = Counter(keywords)
            
            # 获取最大频率，用于标准化颜色
            max_frequency = max(keyword_counts.values(), default=1)  # 防止除以零

            # 格式化为所需的数据结构，并根据频率生成颜色
            result = [{'keyword': keyword, 'frequency': count, 'color': get_color(count, max_frequency)} 
                      for keyword, count in keyword_counts.items()]
            return result
    finally:
        connection.close()

def get_color(frequency, max_frequency):
    """
    根据频率生成深色系的暖色调颜色，频率越高，颜色越暖。
    这里使用 HSL 色调来生成颜色，频率值越大，色相偏向红色、橙色、黄色，且色调为深色。
    """
    # 将频率标准化为 0 到 1 之间
    normalized = frequency / max_frequency
    
    # 根据标准化的频率值生成 HSL 颜色
    # 色相范围从 0 到 60，频率越大，色相越偏向黄色
    hue = int(normalized * 60)  # 色相（0 红色，60 黄色）
    saturation = 80  # 饱和度固定为 80%，确保颜色鲜艳
    # 亮度范围从 20% 到 40%，确保颜色偏暗
    lightness = int(normalized * 20) + 20  # 亮度，频率越高，亮度越高，但仍保持在较低的范围

    # 返回 HSL 颜色格式
    return f"hsl({hue}, {saturation}%, {lightness}%)"


from datetime import datetime, timedelta

def get_contributions():
    """获取近30天每日文章贡献量"""
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # 计算时间范围（包含当天）
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=29)).strftime('%Y-%m-%d')

            # 查询SQL（已添加时区转换）
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
            
            # 转换为字典格式方便查询
            result_dict = {row[0].strftime('%Y-%m-%d'): row[1] for row in db_results}

            # 生成完整30天日期序列
            date_list = [(datetime.now() - timedelta(days=i)).date() 
                       for i in range(29, -1, -1)]

            # 填充数据（包含零值）
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

 

@app.route('/api/contributions', methods=['GET'])
def contributions():
    """贡献趋势数据接口"""
    try:
        contribution_data = get_contributions()
        return jsonify(contributions=contribution_data)
    except Exception as e:
        print(f"获取贡献数据失败: {str(e)}")
        return jsonify(error="服务器内部错误"), 500

@app.route('/api/keywords', methods=['GET'])
def keywords():
    keywords_data = get_keywords()
    # 返回关键词及其频率和颜色的列表
    return jsonify(keywords=keywords_data)

    
import random
from flask import jsonify
from qiniu import Auth, BucketManager

@app.route('/api/music', methods=['GET'])
def list_music():
    try:
        # 初始化 Auth 和 BucketManager
        q = Auth(access_key, secret_key)
        bucket = BucketManager(q)

        # 分页获取所有音乐文件
        limit = 100
        marker = None
        music_files = []

        while True:
            ret, eof, info = bucket.list(bucket_name, prefix='', marker=marker, limit=limit)
            if info.status_code != 200 or not ret or 'items' not in ret:
                return jsonify(error='获取音乐列表失败'), 500

            # 筛选音乐文件
            for item in ret['items']:
                key = item['key']
                if key.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                    music_files.append({
                        'name': key,
                        'url': f"{domain}/{key}"
                    })

            if eof:
                break
            marker = ret.get('marker')  # 下一页的 marker

        if not music_files:
            return jsonify(error='没有找到音乐文件'), 404

        # 随机返回一个
        selected = random.choice(music_files)
        return jsonify(music=selected)

    except Exception as e:
        print(f"七牛云获取音乐文件失败: {str(e)}")
        return jsonify(error="服务器内部错误"), 500
   


if __name__ == '__main__':
    app.run(debug=True)
