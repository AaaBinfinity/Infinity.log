from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 允许所有来源的请求
    CORS(app)
    
    # 注册蓝图
    from .routes.quiz import quiz_bp
    from .routes.quotes import quotes_bp
    from .routes.titles import titles_bp
    from .routes.keywords import keywords_bp
    from .routes.images import images_bp
    from .routes.contributions import contributions_bp
    from .routes.music import music_bp
    
    app.register_blueprint(quiz_bp)
    app.register_blueprint(quotes_bp)
    app.register_blueprint(titles_bp)
    app.register_blueprint(keywords_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(contributions_bp)
    app.register_blueprint(music_bp)
    
    return app