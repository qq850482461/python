from flask_script import Manager
from werkzeug.utils import secure_filename
from app import create_app
app = create_app()
manager = Manager(app)
@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)



if __name__ == '__main__':
    # app.run(port=80,debug = True)
    # manager.run()
    dev()
