from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from urllib.parse import unquote
from app import app, db
from app.forms import LoginForm, DomainForm, LogFormUpload
from app.models import User, Domain, LogStorage
import os
import re
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    Index page
    """
    stats = {'total_domains': Domain().get_total_domains(),
             'total_logs': LogStorage().get_total_logs()}
    form = DomainForm()
    if form.validate_on_submit():
        domain = Domain(domain_name=form.domain.data)
        db.session.add(domain)
        db.session.commit()
        flash('Domain added!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form, stats=stats)


@app.route('/domains/<int:domain_id>')
@login_required
def domains(domain_id):
    """
    Domain page
    """
    domain = Domain.query.get_or_404(domain_id)
    form = LogFormUpload(domain_id=domain_id)
    return render_template('domain_details.html', title='Domain', domain_details=domain, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in the user
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    Logs out the user
    """
    logout_user()
    return redirect(url_for('index'))


### FILE HANDLING ###
@app.route('/logUpload', methods=['POST'])
def logUpload():
    """
    Uploads the log file
    """
    form = LogFormUpload()
    if form.validate_on_submit():
        log_file = form.log.data
        filename = log_file.filename
        upload_path = app.config['UPLOAD_PATH']
        log_file.save(os.path.join(upload_path, filename))
        logs = LogStorage(file_location=filename, domain_id=form.domain_id.data,
                          created_at=datetime.now())
        # return str(x)
        db.session.add(logs)
        db.session.commit()
        flash('Log file uploaded!')
        return redirect('domains/' + str(form.domain_id.data) + '')

### API ###


@app.route('/api/parse_log_file/<int:log_id>')
@login_required
def parse_log_file(log_id):
    """
    Returns a list of log file data in JSON format
    """
    log = LogStorage.query.get_or_404(log_id)
    data = {'data': [{'id': log.id, 'file_location': log.file_location,
                      'created_at': log.created_at.strftime('%Y-%m-%d %H:%M:%S')}]}
    with open(os.path.join(app.config['UPLOAD_PATH'], log.file_location), 'r') as f:
        datas = f.read()
        pattern = r'(\S+) (\S+) (\S+) \[(.*?)\] "(\S+) (\S+) (\S+)" (\S+) (\S+) "(\S+)" "(.*?)"'
        all_logs_parsed = []
        for x in datas.split('\n'):
            match = re.search(pattern, x)
            if match:
                all_logs_parsed.append(
                    {
                        'ip_address': str(match.group(1)),
                        'method': str(match.group(5)),
                        'path': unquote(str(match.group(6))),
                        'status_code': str(match.group(8)),
                        'http_version': str(match.group(7)),
                        'user_agent': str(match.group(11)),
                        'date_str': str(datetime.strptime(match.group(4), '%d/%b/%Y:%H:%M:%S %z').date())
                    }
                )
        data['data'][0]['logs'] = all_logs_parsed

    return jsonify(data)


@app.route('/api/domains_list')
@login_required
def domains_list():
    """
    Returns a list of domains in JSON format
    """
    domains = Domain.query.all()
    data = {'data': [{'id': domain.id, 'domain_name': domain.domain_name, 'actions': '<a href="/domains/' + str(domain.id) + '" class="btn btn-info btn-sm">See Log</a>'}
            for domain in domains]}
    return jsonify(data)


@app.route('/api/domain_storage/<int:domain_id>')
@login_required
def domain_storage(domain_id):
    """
    Returns a list of log files for a domain in JSON format
    """
    Logs = LogStorage.query.filter_by(domain_id=domain_id).all()
    data = {'data': [{'id': log.id, 'file_location': log.file_location, 'created_at': log.created_at.strftime('%Y-%m-%d %H:%M:%S'), 'analyze_btn': '<a href="/analyze_log_file/' + str(log.id) + '" class="btn btn-warning btn-sm">Analyze</a>', 'delete_btn': '<a href="/delete_log_file/' + str(log.id) + '" class="btn btn-danger btn-sm">Delete</a>'}
            for log in Logs]}
    return jsonify(data)
