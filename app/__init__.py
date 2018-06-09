from app import settings
from app.ext import init_ext
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.Config)

    #初始化第三方插件
    init_ext(app)

    return app