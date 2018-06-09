from app import dao,ext


from app.helper import getToken
from app.models import User
from celery import Celery
# from app.models import
from flask import request, render_template
from flask_mail import Message

try:
    import manage
except:
    pass
celery = Celery('tasks',
                broker='redis://10.35.163.12:6379/8',
                )
@celery.task
def sendMail(uId):
    with manage.app.test_request_context():
        u = dao.getById(User,uId)
        token = getToken()
        ext.cache.set(token, u.id, timeout=60)  # ???
        active_url = request.host_url + 'account/?opt=active&token=' + token
        # 发送邮件
        msg = Message(subject='tpp用户激活',
                      recipients=[u.email],
                      sender='13659194116@163.com')
        # msg.html = '<h1>{}注册成功</h1><h3>请先<a href={}>激活</a>注册账号</h3><h2>或者复制地址到浏览器：{}</h2>'.format(u.name, active_url,active_url)
        msg.html = render_template('msg.html', user=u, active_url=active_url)

        try:
            ext.mail.send(msg)
            print('邮件已发送')
        except Exception as e:
            print(e)



