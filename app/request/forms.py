from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField
from wtforms import SubmitField, validators
# from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Service


class RequestForm(Form):
    '''This class creates an RequestForm
    object.
    '''

    name = StringField('Request',
                       [validators.Required(message='We need an Request.'),
                        validators.Length(
                           max=70,
                           message='Your \subject is a tad long.'
                       )
                       ]
                       )
    description = TextAreaField('Request Description',
                                [validators.required(
                                    message='Please describe your Request.')])
    priority = SelectField('Priority', choices=[
        ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')])
    department = SelectField('Department',
                             [validators.Required(
                                 message='Department required.')],
                             coerce=int)
    service = SelectField('Service',
                             [validators.Required(
                                 message='Service required.')],
                             coerce=int)
    submit = SubmitField('Post Request')

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.department.choices = [
            (dept.id, dept.name) for dept in Department.query.all()]
        self.service.choices = [
            (service.id, service.name) for service in Service.query.all()]


class CommentForm(Form):
  '''This class creates a CommentForm
  object
  '''
  comment = TextAreaField('Comment')