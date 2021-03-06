#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Team, Flag, Solve, Chal, Role
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
server = Server(port=5001)


def make_shell_context():
    return dict(app=app, db=db, User=User, Team=Team, Flag=Flag, Solve=Solve, Chal=Chal)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', server)

if __name__ == '__main__':
    manager.run()
