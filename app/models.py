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
    domain_id = db.Column(db.Integer, db.ForeignKey(
        'domains_db.id'), nullable=False)
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
