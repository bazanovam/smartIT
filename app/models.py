from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Comments(db.Model):
    '''This class creates comment objects
    associated with a user.
    '''

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                           backref=db.backref('comments', lazy='dynamic'))


class Department(db.Model):
    '''This class creates a department
    object.
    '''
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    dept_head = db.Column(db.Integer)

class Status(db.Model):
    '''This class creates a status
    object.
    '''
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class Service(db.Model):
    '''This class creates a service
    object.
    '''
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class Issue(db.Model):
    '''This class creates issues objects
    by user object
    '''
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    priority = db.Column(db.String(10))
    closed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                           backref=db.backref('issues', lazy='dynamic'))

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    # #department = db.relationship('Department',
    #                              backref=db.backref('departments',
    #                                                 lazy='dynamic'))

class Request(db.Model):
    '''This class creates Request objects
    by user object
    '''
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70))
    description = db.Column(db.Text)
    priority = db.Column(db.String(10))
    
    closed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    department = db.relationship('Department', backref='departments')

    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    status = db.relationship('Status', backref=db.backref('requests', lazy='dynamic'))

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    service = db.relationship('Service', backref=db.backref('requests', lazy='dynamic'))



class Role(db.Model):
    '''This class creates a User Role object
    '''
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.name


class User(UserMixin, db.Model):
    '''This class creates a user object
    associated with a Role object
    '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role',
                           backref=db.backref('users', lazy='dynamic'))

    @property
    def password(self):
        '''prevents access to password
        property
        '''
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        '''Sets password to a hashed password
        '''
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        '''Checks if password matches
        '''
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
