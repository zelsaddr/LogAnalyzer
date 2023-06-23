from app import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'user_db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    password_hash = db.Column(db.String(255))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Domain(db.Model):
    __tablename__ = 'domains_db'
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Domain {}>'.format(self.domain_name)

    def add_domain(self, domain):
        self.domain_name = domain

    def get_domain(self, domain_id):
        return Domain.query.filter_by(id=domain_id).first()

    def get_total_domains(self):
        return Domain.query.count()


class LogStorage(db.Model):
    __tablename__ = 'logs_storage_db'
    id = db.Column(db.Integer, primary_key=True)
    file_location = db.Column(db.String(255), nullable=False)
    domain_id = db.Column(db.Integer, nullable=False)
    analyzed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<LogStorage {}>'.format(self.file_location)

    def add_file_location(self, file_location):
        self.file_location = file_location

    def add_domain_id(self, domain_id):
        self.domain_id = domain_id

    def add_created_at(self, created_at):
        self.created_at = created_at

    def get_total_logs(self):
        return LogStorage.query.count()


class Patterns(db.Model):
    __tablename__ = 'patterns_db'
    id = db.Column(db.Integer, primary_key=True)
    pattern_name = db.Column(db.String(50), nullable=False)
    pattern_syntax = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Patterns {}>'.format(self.pattern)

    def add_pattern(self, pattern):
        self.pattern = pattern

    def get_total_patterns(self):
        return Patterns.query.count()


class LogsDetails(db.Model):
    __tablename__ = 'logs_details_db'
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer)
    logs_storage_id = db.Column(db.Integer)
    log_text = db.Column(db.String(255))
    ip_address = db.Column(db.String(100))
    date = db.Column(db.String(255))
    method = db.Column(db.String(255))
    url = db.Column(db.String(255))
    status_code = db.Column(db.String(30))
    user_agent = db.Column(db.String(255))
    log_type = db.Column(db.String(255))
    uagent_bot = db.Column(db.String(100))

    def __repr__(self):
        return '<LogsDetails {}>'.format(self.log_text)

    def add_domain_id(self, domain_id):
        self.domain_id = domain_id

    def add_logs_storage_id(self, logs_storage_id):
        self.logs_storage_id = logs_storage_id

    def add_log_text(self, log_text):
        self.log_text = log_text

    def add_ip_address(self, ip_address):
        self.ip_address = ip_address

    def add_date(self, date):
        self.date = date

    def add_method(self, method):
        self.method = method

    def add_url(self, url):
        self.url = url

    def add_status_code(self, status_code):
        self.status_code = status_code

    def add_user_agent(self, user_agent):
        self.user_agent = user_agent

    def add_log_type(self, log_type):
        self.log_type = log_type

    def get_total_logs_details(self):
        return LogsDetails.query.count()

    def get_total_logs_details_by_domain(self, domain_id):
        return LogsDetails.query.filter_by(domain_id=domain_id).count()
