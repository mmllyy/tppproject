import hashlib
import uuid

from flask import request, app, render_template
from flask_mail import Message
import app.ext


def md5_crypt(txt):
    m = hashlib.md5()
    m.update(txt.encode())
    return m.hexdigest()

def getToken():
    return md5_crypt(str(uuid.uuid4()))

def sendEmail(u):
    token = getToken()
    app.ext.cache.set(token, u.id, timeout=60)  # ???
    active_url = request.host_url + 'account/?opt=active&token=' + token
    # 发送邮件
    msg = Message(subject='tpp用户激活',
                  recipients=[u.email],
                  sender='13659194116@163.com')
    # msg.html = '<h1>{}注册成功</h1><h3>请先<a href={}>激活</a>注册账号</h3><h2>或者复制地址到浏览器：{}</h2>'.format(u.name, active_url,active_url)
    msg.html = render_template('msg.html',user=u,active_url=active_url)
    try:
        app.ext.mail.send(msg)
    except Exception as e:
        print(e)
