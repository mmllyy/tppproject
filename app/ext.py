# 集成第三方
from app.apis import init_api
from app.models import init_db
from flask_cache import Cache
from flask_mail import Mail

mail = Mail()
cache = Cache(config={
    'CACHE_TYPE':'redis',
    'CACHE_REDIS_HOST':'10.35.163.12',
    'CACHE_REDIS_DB':12

})
def init_ext(app):
    # db.init_app(app)
    # migrate.init_app(app,db)
    init_db(app)
    init_api(app)
    mail.init_app(app)
    cache.init_app(app)