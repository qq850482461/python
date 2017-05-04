from flask_script import Manager #flask 脚本
from flask_migrate import Migrate,MigrateCommand #flask 迁移数据
from app import create_app,db

app = create_app()
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)#增加"db"命令


#创建数据库
@manager.command
def create_db():
    db.create_all()



@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)



if __name__ == '__main__':
    # app.run()
    manager.run()
