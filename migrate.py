from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flaskblog import db, app, create_app

db.create_all()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# from flaskblog import users, posts

if __name__ == '__main__':
    manager.run()
