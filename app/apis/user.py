import uuid

import tasks
from app import helper, dao

from app.models import User
from flask import request, app
from flask_mail import Message
from flask_restful import Resource, reqparse
import app.ext


class UserApi(Resource):
    #定制输入
    parser = reqparse.RequestParser()
    parser.add_argument('username',dest='name',required = True,help='用户名不能为空')

    def post(self):
        registParser = self.parser.copy()
        registParser.add_argument('password', dest='pwd', required=True, help='密码不能为空')
        registParser.add_argument('email', required=True, help='邮箱不能为空')
        registParser.add_argument('phone', required=True, help='电话不能为空')
        registParser.add_argument('nickname', required=True, help='昵称不能为空')

        args = registParser.parse_args()
        u = User()
        u.name = args.get('name')
        u.nickName = args.get('nickname')
        u.email = args.get('email')
        u.phone = args.get('phone')
        u.password = helper.md5_crypt(args.get('pwd'))
        if dao.save(u):
            # helper.sendEmail(u)
            tasks.sendMail.delay(u.id)
            return {'status':200,
                    'msg':'用户注册成功'}
        return {'status': 201,
                'msg': '用户注册失败'}

    def get(self):
        args = self.parser.parse_args()
        name =args.get('name')
        qs = dao.query(User).filter(User.name==name)
        if qs.count():
            return {'status':202,'msg':name+'用户名不可用'}
        return {'status': 200, 'msg': name + '用户名可用'}










