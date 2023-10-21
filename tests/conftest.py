# conftest.py
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


@pytest.fixture(scope='module')
def app_instance():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    from .models import User, Role, Permission, RolePermission, Project, UserRole
    return app

@pytest.fixture(scope='module')
def db_session(app_instance):
    with app_instance.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.session.remove()
        db.drop_all()
