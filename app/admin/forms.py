from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, SelectField
from wtforms import IntegerField
from ..models import User


class DepartmentForm(Form):
    '''This class creates a new Department
    Form object
    '''
    name = StringField('Department Name', [validators.Required()])
    dept_head = SelectField('Department Head', coerce=int)    
    submit = SubmitField('Create Department')

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.dept_head.choices = [
            (user.id, user.username) for user in User.query.all()
        ]

class StatusForm(Form):
    '''This class creates a new Status
    Form object
    '''
    name = StringField('Status Name', [validators.Required()])
    submit = SubmitField('Create Status')

    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        # self.dept_head.choices = [
        #     (user.id, user.username) for user in User.query.all()
        # ]

class ServiceForm(Form):
    '''This class creates a new service
    Form object
    '''
    name = StringField('Service Name', [validators.Required()])
    submit = SubmitField('Create Service')