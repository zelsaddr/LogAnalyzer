from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, DomainForm
from app.models import User, Domain


@login_required
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    stats = {'total_domains': Domain().get_total_domains()}
    form = DomainForm()
    if form.validate_on_submit():
        domain = Domain(domain_name=form.domain.data)
        db.session.add(domain)
        db.session.commit()
        flash('Domain added!')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form, stats=stats)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    logout_user()
    return redirect(url_for('index'))


@app.route('/api/domains_list')
def domains_list():
    domains = Domain.query.all()
    data = {'data': [{'id': domain.id, 'domain_name': domain.domain_name, 'actions': '<a href="/see/' + str(domain.id) + '" class="btn btn-info btn-sm">See Log</a>'}
            for domain in domains]}
    return jsonify(data)
