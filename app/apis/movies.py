from app import dao
from app.models import Movies, User, Qx
from app.settings import QX
from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import BaseQuery


def check_login(qx):
    def check(fun):
        def wrapper(*args, **kwargs):
            # wrapperActive = MoviesApi.parser.copy()
            # wrapperActive.remove_argument('flag')
            # args = wrapperActive.parse_args()
            print('--check login--')
            token = request.form.get('token')
            if not token:
                token=request.args.get('token')
            user_id = session.get(token)
            if not user_id:
                return {'msg': '用户必须先登录'}
            loginUser: User = dao.getById(User, user_id)
            if loginUser.rights & qx == qx:
                return fun(*args, **kwargs)
            else:
                qxObj = dao.query(Qx).filter(Qx.right == qx).first
                return {'msg': '用户没有{}权限'.format(qxObj.name)}

        return wrapper

    return check



class MoviesApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('token')
    parser.add_argument('flag', type=int, required=True, help='必须提供flag参数')
    parser.add_argument('city', default='')
    parser.add_argument('region', default='')
    parser.add_argument('sort', type=int, default=1)  # 1 降序 0 升序
    parser.add_argument('orderby', default='openday')
    parser.add_argument('page', type=int, default=1, help='页码必须int类型')
    parser.add_argument('limit', default=10, type=int, help='每页显示数量必须int类型')

    out_fields = {
        'returnCode': fields.String(default='0'),
        'returnValue': fields.Nested({
            'backgroundPicture': fields.String,
            'country': fields.String,
            'director': fields.String,
            'showName': fields.String(attribute='showname'),
            'openTime': fields.DateTime(attribute='openday')

        })

    }

    @marshal_with(out_fields)
    def get(self):
        args = self.parser.parse_args()
        flag = args.get('flag')
        # if flag==0:
        qs: BaseQuery = dao.query(Movies).filter(Movies.flag == flag)

        sort = args.get('sort')
        qs: BaseQuery = qs.order_by(('-' if sort == 1 else '') + args.get('orderby'))

        # 分页
        pager = qs.paginate(args.get('page'), args.get('limit'))
        return {'returnValue': pager.items}

    @check_login(QX.DELETE_QX)
    def delete(self):
        # 删除影片功能
        # mid = request.args.get('mid')
        # 从session里拿token
        # user_id = session.get(request.args.get('token'))
        # if not user_id:
        #     return {'msg':'请先登录'}
        # loginUser:User = dao.getById(User,user_id)
        # if loginUser.rights & QX.DELETE_QX == QX.DELETE_QX:
        #     movie = dao.getById(Movies,mid)
        #     if not movie:
        #         return {'msg':'影片不存在'}
        #     dao.delete(movie)
        #     return {'msg':'删除成功'}
        # return {'msg':'你没有删除权限'}
        mid = request.args.get('mid')
        movie = dao.getById(Movies, mid)
        if not movie:
            return {'msg': '影片不存在'}
        dao.delete(movie)
        return {'msg': '删除成功'}

    def check_in(self,qx):
        addmovie = self.parser.copy()
        # addmovieAction.remove_argument('flag')
        addmovie.remove_argument('limit')
        addmovie.add_argument('mId', type=int, required=True, help='必须提供电影id')
        addmovie.add_argument('showname', required=True, help='必须提供电影名')
        addmovie.add_argument('showname', required=True, help='必须提供电影名')
        addmovie.add_argument('shownameen', required=True, help='必须提供电影英文名')
        addmovie.add_argument('director', required=True, help='必须提供导演名')
        addmovie.add_argument('leadingRole', required=True, help='必须提供导主演')
        addmovie.add_argument('type', required=True, help='必须提供电影类型')
        addmovie.add_argument('country', required=True, help='必须提供国家')
        addmovie.add_argument('language', required=True, help='必须提供语言')
        addmovie.add_argument('duration', type=int, required=True, help='必须提供int类型的参数')
        addmovie.add_argument('screeningmodel', required=True, help='必须提供上映模式')
        addmovie.add_argument('openday', required=True, help='必须提供上映时间')
        addmovie.add_argument('backgroundpicture', required=True, help='必须提供背景图片')
        addmovie.add_argument('isdelete', default=0)
        addmovie.add_argument('opt', required=True, help='请指定操作')

        args=addmovie.parse_args()
        movie=dao.getById(Movies,args.get('mId'))
        if qx==QX.ADD_QX:
            if movie:
                return {'msg':'你添加的电影存在'}
            movie = Movies()
        elif qx==QX.EDIT_QX:
            if not movie:
                return {'msg':'你要修改的电影不存在'}

        for key,value in args.items():
            if hasattr(movie,key):
                setattr(movie,key,value)
                dao.save(movie)
        return {'msg':('添加' if qx==QX.ADD_QX else '修改')+'成功'}


    def post(self):
        postActive=self.parser.copy()
        postActive.remove_argument('flag')
        postActive.add_argument('opt')
        args=postActive.parse_args()
        opt = args.get('opt')
        if opt == 'addmovie':
            return self.addmovie()
        else:
            return self.modifymovie()


    @check_login(QX.ADD_QX)
    def addmovie(self):
        return self.check_in(QX.ADD_QX)


    @check_login(QX.EDIT_QX)
    def modifymovie(self):
        return self.check_in(QX.EDIT_QX)






