from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from mm import db, app, create_app

db.create_all()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# from Models import Roles, Users, RevokedTokens

if __name__ == '__main__':
    manager.run()
