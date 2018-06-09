import uuid
from datetime import datetime

import os
from app import dao, helper, settings
from app.models import User
from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal
import app.ext
from werkzeug.datastructures import FileStorage


class AccountApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('opt',required=True,help='没有声明opt的操作')
    # parser.add_argument('token')

    def get(self):
        # 从请求参数中获取opt和token参数值
        # 如果opt 为active ，则从redis缓存中查询token对应的user.id
        # 再通过 user.id查询数据库中用户， 最后更新用户的is_active状态为True
        args = self.parser.parse_args()
        opt = args.get('opt')
        if opt == 'active':
            avtiveParser = self.parser.copy()
            avtiveParser.add_argument('token',required = True,help='必须提供激活的token')
            args = avtiveParser.parse_args()

            token = args.get('token')
            print(token)
            user_id = app.ext.cache.get(token)
            print(user_id)
            if user_id:
                user = dao.getById(User,user_id)
                print(user)
                user.is_active = True
                dao.save(user)
                return {'msg':user.nickName+'激活成功'}
            else:
                active_url = request.host_url + 'account/?opt=reactive'
                return {'msg': '本次激活已过期，需要重新申请激活'+active_url}

        elif opt == 'login':
            return self.login()

        elif opt == 'reactive':
            return self.reactive()

        elif opt == 'logout':
            return self.logout()

    def login(self):
        loginParser = self.parser.copy()
        loginParser.add_argument('name', required=True, help='必须提供name')
        loginParser.add_argument('password', required=True, help='必须提供password')

        args = loginParser.parse_args()
        username = args.get('name')
        password = args.get('password')
        qs = dao.query(User).filter(User.name==username,
                                    User.password==helper.md5_crypt(password),
                                    User.is_active ==True,
                                    User.is_life == True)
        if not qs.count():
            return {'status': 600, 'msg': '用户登录失败，用户名或口令不正确！'}
        u:User = qs.first()
        u.last_login_time = datetime.today()
        dao.save(u)
        token = helper.getToken()
        session[token] = u.id  # 将token存放session中
        out_user_fields = {
            'name':fields.String,
            'email':fields.String,
            'phone':fields.String,
            'photo':fields.String(attribute='photo_1')
        }
        out_fields = {
            'msg':fields.String,
            'data':fields.Nested(out_user_fields),
            'access_token':fields.String
        }
        data = {'msg':'登录成功',
                'data': u,
                'access_token': token}
        return marshal(data, out_fields)

    def reactive(self):
        reactiveParser = self.parser.copy()
        reactiveParser.add_argument('email',required=True, help='必须提供email')
        args = reactiveParser.parse_args()
        email = args.get('email')
        qs = dao.query(User).filter(User.email.__eq__(email))
        if not qs.count():
            return {'status': 700, 'msg': email + '邮箱未被注册'}
            # 重新发送邮件
        helper.sendEmail(qs.first())
        return {'msg': '重新申请用户激活，请查收邮箱激活'}

    def logout(self):
        myParser = self.parser.copy()
        myParser.add_argument('token', required=True, help='用户退出必须提供token参数')

        args = myParser.parse_args()
        token = args.get('token')
        user_id = session.get(token)
        if not user_id:
            return {'status': 701, 'msg': '用户未登录，请先登录!'}

        u = dao.getById(User, user_id)
        if not u:
            return {'status': 702, 'msg': '用户退出失败，token无效!'}

        session.pop(token)  # 从session中删除token
        return {'status': 200, 'msg': '退出成功!'}

    def post(self):
        parserImg = self.parser.copy()
        parserImg.remove_argument('opt')
        parserImg.add_argument('token')
        parserImg.add_argument('img',type=FileStorage,location='files',required=True,help='必须选择要上传的文件')
        args = parserImg.parse_args()
        img:FileStorage = args.get('img')
        print(img)
        imgName = str(uuid.uuid4()).replace('-','')
        imgName += '.'+ img.filename.split('.')[-1]
        img.save(os.path.join(settings.MEDIA_DIR,imgName))
        imgPath = '/app/static/uploads/'+imgName
        token = args.get('token')
        user_id = session.get(token)
        print('我的id是',user_id)
        qs = dao.getById(User,user_id)
        if not qs:
            return {'status':201,
                    'msg':'请先登录'}
        qs.photo_1 = imgPath
        dao.save(qs)
        return {
            'status': 200,
            'imgpath': imgPath
        }

