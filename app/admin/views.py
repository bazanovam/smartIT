from flask import render_template, flash
from flask_login import login_required, current_user
from . import admin
from .. import db
from ..models import Issue, User, Department, Status, Service
from .forms import DepartmentForm, StatusForm, ServiceForm


@admin.route('/users')
@login_required
def users():
    '''View function to return all users.
    '''
    users_ = User.query.all()
    return render_template('admin/users.html', users_=users_)


@admin.route('/issues')
@login_required
def issues():
    issues_ = Issue.query.all()
    return render_template('admin/issues.html', issues_=issues_)


@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():    
    form = DepartmentForm()
    if form.validate_on_submit():
        # check if department exists
        dept = Department.query.filter_by(name=form.name.data).first()
        if dept is None:
            curr_user = current_user.id
            department = Department(name=form.name.data,
                                    dept_head=form.dept_head.data)
            department.creator = curr_user
            db.session.add(department)
            db.session.commit()
            flash('Department added successfully.')
    # check for departments.
    departments_ = Department.query.all()
    return render_template('admin/departments.html',
                           departments_=departments_,
                           form=form)


@admin.route('/statuses', methods=['GET', 'POST'])
@login_required
def statuses():    
    form = StatusForm()
    if form.validate_on_submit():
        # check if status exists
        status = Status.query.filter_by(name=form.name.data).first()
        if status is None:
            curr_user = current_user.id
            status_ = Status(name=form.name.data)
            status_.creator = curr_user
            db.session.add(status_)
            db.session.commit()
            flash('Status added successfully.')
    # check for departments.
    statuses_ = Status.query.all()
    return render_template('admin/statuses.html',
                           statuses_=statuses_,
                           form=form)

@admin.route('/services', methods=['GET', 'POST'])
@login_required
def services():    
    form = ServiceForm()
    if form.validate_on_submit():
        # check if status exists
        service = Service.query.filter_by(name=form.name.data).first()
        if service is None:
            curr_user = current_user.id
            service_ = Service(name=form.name.data)
            service_.creator = curr_user
            db.session.add(service_)
            db.session.commit()
            flash('Service added successfully.')
    # check for departments.
    services_ = Service.query.all()
    return render_template('admin/services.html',
                           services=services_,
                           form=form)
