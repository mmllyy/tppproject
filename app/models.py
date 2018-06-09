#
from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()
def init_db(app):
    # db.init_app(app)
    #
    # migrate.init_app(app,db)
    db.init_app(app)
    Migrate(app,db)

class IdBase():
    id = Column(Integer,primary_key=True,autoincrement=True)

class Letter(db.Model,IdBase):
    # __tabkename__ = 't_letter'
    # id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(10))


class City(db.Model,IdBase):
    # __tabkename__ = 't_city'
    # id = Column(Integer,primary_key=True,autoincrement=True)
    parentId = Column(Integer,default=0)
    refionName = Column(String(20))
    cityCode = Column(Integer)
    pinYin = Column(String(50))

    letter_id = Column(Integer,ForeignKey(Letter.id))
    letter = relationship('Letter',
                          backref = backref('citys',lazy=True))


class Role(db.Model,IdBase):
    # 用户角色
    name = Column(String(20))
    rights = Column(Integer,default=1)


class User(db.Model,IdBase):
    __tablename__='t_user'
    # id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=True)
    password = Column(String(50))
    nickName = Column(String(20))
    email = Column(String(50),unique=True)
    phone = Column(String(12),unique=True)
    is_active =Column(Boolean,default=False)
    is_life = Column(Boolean,default=True)
    regist_time = Column(DateTime,default=datetime.now())
    last_login_time = Column(DateTime)
    # 新增头像属性
    photo_1 = Column(String(200),nullable=True) # 原图
    photo_2 = Column(String(200),nullable=True) # 小图
    # 权限(被管理员授权)
    rights = Column(Integer,default=1)
    # 用户角色
    role_id = Column(Integer,ForeignKey(Role.id))
    role = relationship('Role',
                        backref=backref('users',lazy = True))



class Movies(db.Model,IdBase):
    '''
    insert into movies(id, showname, shownameen, director,
     leadingRole, type, country, language,
     duration, screeningmodel, openday,
      backgroundpicture, flag, isdelete)
    values(228830,"梭哈人生","The Drifting Red Balloon",
    "郑来志","谭佑铭,施予斐,赵韩樱子,孟智超,李林轩","剧情,爱情,喜剧",
    "中国大陆","汉语普通话",90,"4D",date("2018-01-30 00:00:00"),
    "i1/TB19_XCoLDH8KJjy1XcXXcpdXXa_.jpg",1,0);

    '''
    showname = Column(String(100))
    shownameen = Column(String(200))
    director = Column(String(50))
    leadingRole = Column(String(300))
    type = Column(String(50))
    country = Column(String(20))
    language = Column(String(20))
    duration = Column(Integer)
    screeningmodel = Column(String(20))
    openday = Column(DateTime)
    backgroundpicture = Column(String(200))
    flag = Column(Integer)
    isdelete = Column(Boolean)


class Cinemas(db.Model,IdBase):
    '''
    insert into cinemas
    (name,city,district,address,phone,score,
    hallnum,servicecharge,astrict,flag,isdelete)
     values("深圳戏院影城","深圳","罗湖",
     "罗湖区新园路1号东门步行街西口","0755-82175808",
     9.7,9,1.2,20,1,0);

    '''
    name = Column(String(50))
    city = Column(String(20))
    district = Column(String(20))
    address = Column(String(200))
    phone = Column(String(50))
    score = Column(Float(precision=1))
    hallnum = Column(Integer)
    servicecharge = Column(Float(precision=2))
    astrict = Column(Integer,default=5)
    flag =  Column(Integer)
    isdelete = Column(Boolean,default=False)


class Qx(db.Model,IdBase):
    name = Column(String(30))
    right = Column(Integer)
    # query_qx = Column(Boolean)







