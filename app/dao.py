# coding:utf-8
#定义操作数据库的功能函数
from app.models import db
from flask_sqlalchemy import BaseQuery




def query(cls) -> BaseQuery:
    #返回基于某一类的查询
    return db.session.query(cls)

def queryAll(cls):
    #返回所有查询
    return query(cls).all()

# def queryByWhere(cls,**where):
#     return query(cls).filter(where)

def getById(cls,id):
    try:
        return query(cls).get(int(id))
    except:
        return False

def save(obj) -> bool:
    try:
        db.session.add(obj)
        db.session.commit()
    except:
        return False

    return True

def delete(obj) -> bool:
    try:
        db.session.delete(obj)
        db.session.commit()
    except:
        return False
    return True
