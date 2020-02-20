#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Department, Request
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    '''Returns application and database instances
    to the shell importing them automatically
    on `python manager.py shell`.
    '''
    return dict(app=app, db=db, User=User, Role=Role,
                Department=Department, Request=Request)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
print('test')


if __name__ == '__main__':
    manager.run()
