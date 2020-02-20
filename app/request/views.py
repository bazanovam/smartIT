from flask import render_template, redirect, request as http_request, url_for, flash
from flask_login import login_required, current_user
from . import request
from .. import db
from ..models import Request, User, Status
from .forms import RequestForm


@request.route('/request')
@login_required
def index():
    '''This view function displays
    requests records in the database.
    '''
    state = http_request.args.get('state')
    statuses = Status.query.all()
    requests_ = Request.query.all()
    closed_requests = 0
    open_requests = 0
    
    requests_filtered = []
    for i in requests_:
        if i.closed:
            closed_requests += 1
            if state == 'closed':
                requests_filtered.append(i)
        else:
            open_requests += 1
            if state == 'open':
                requests_filtered.append(i)
    if state is None:
        requests_filtered = requests_

    total_requests = closed_requests + open_requests
    return render_template('request/index.html', requests_=requests_filtered,
                           total_requests=total_requests,
                           closed_requests=closed_requests,
                           open_requests=open_requests,
                           statuses=statuses)

@request.route('/view')
@login_required
def view():
    '''This view function displays
    requests records in the database.
    '''
    id_ = http_request.args.get('request_id')
    request_ = Request.query.filter_by(id=id_).first()
   
    return render_template('request/view_request.html', request=request_)

@request.route('/request/closed', methods=['GET', 'POST'])
@login_required
def closed():
    if http_request.method == 'POST':
        id_ = http_request.form.get('cl')
        status_ = http_request.form.get('status')
        print(status_)
        request = Request.query.filter_by(id=id_).first()
        request.status_id = status_
        if status_ == '6':
            request.closed = True
        else:
            request.closed = False

        db.session.add(request)
        db.session.commit()
        return redirect(http_request.args.get('next') or url_for('request.index'))


@request.route('/request/me')
@login_required
def my_request():
    '''This view function displays
    requests records in the database
    specific to a user
    '''
    user = User.query.filter_by(id=current_user.id).first()
    requests_ = user.requests.all()
    closed_requests = 0
    open_requests = 0

    for i in requests_:
        if i.closed:
            closed_requests += 1
        else:
            open_requests += 1
    total_requests = closed_requests + open_requests
    return render_template('request/index.html',
                           requests_=requests_,
                           total_requests=total_requests,
                           closed_requests=closed_requests,
                           open_requests=open_requests)


@request.route('/request/new', methods=['GET', 'POST'])
@login_required
def request():
    '''This view function creates a
    new request record and displays
    current user requests.
    '''
    form = RequestForm()
    if form.validate_on_submit():
        user = current_user.id
        request_ = Request(name=form.name.data,
                       description=form.description.data,
                       priority=form.priority.data,
                       status_id=1,
                       service_id=form.service.data,
                       department_id=form.department.data,
                       user_id=user)
        # import ipdb; ipdb.set_trace()
        db.session.add(request_)
        db.session.commit()
        flash('request posted successfully.')
        return redirect(http_request.args.get('next') or url_for('request.index'))

    user = User.query.filter_by(id=current_user.id).first()
    requests_ = user.requests.all()
    closed_requests = 0
    open_requests = 0

    for i in requests_:
        if i.closed:
            closed_requests += 1
        else:
            open_requests += 1
    total_requests = closed_requests + open_requests
    return render_template('request/new_request.html',
                           form=form, requests_=requests_,
                           total_requests=total_requests,
                           closed_requests=closed_requests,
                           open_requests=open_requests)
