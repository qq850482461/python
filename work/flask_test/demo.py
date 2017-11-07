from .app import db,create_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from work.flask_test.app.models import Test

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app,Test=Test)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)



if __name__ == "__main__":
    manager.run()