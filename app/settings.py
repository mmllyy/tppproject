import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
STATIC_DIR = os.path.join(BASE_DIR,'app/static')
MEDIA_DIR = os.path.join(STATIC_DIR,'uploads')


class Config():
    ENV = 'development'
    DEBUG = True
    #配置数据库连接
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@10.35.163.12:3306/tpp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #配置邮箱
    MAIL_SERVER='smtp.163.com'
    MAIL_USERNAME='13659194116@163.com'
    MAIL_PASSWORD = '1202120324MA'

    #配置安全密钥
    SECRET_KEY = 'bdgfrsrughsu'

class QX():
    QUERY_QX = 1
    EDIT_QX = 2
    DELETE_QX = 4
    ADD_QX = 8
    MAIL_QX = 16
    PLAY_QX = 32

