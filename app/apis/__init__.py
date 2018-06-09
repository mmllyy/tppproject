from app.apis.account import AccountApi
from app.apis.city import CityApi
from app.apis.movies import MoviesApi
from app.apis.user import UserApi
from flask_restful import Api

api = Api()

def init_api(app):
    api.init_app(app)

api.add_resource(CityApi,'/city/')
api.add_resource(UserApi,'/user/')
api.add_resource(AccountApi,'/account/')
api.add_resource(MoviesApi,'/movies/')