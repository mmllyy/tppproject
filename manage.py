from app import create_app
from flask_migrate import MigrateCommand
from flask_script import Manager
try:
    from app import create_app
except:
    pass

app = create_app()
manage = Manager(app)

#添加db迁移的命
manage.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manage.run()
