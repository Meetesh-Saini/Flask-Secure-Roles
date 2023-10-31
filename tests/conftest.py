# conftest.py
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_secure_roles import FlaskSecureRoles

db = SQLAlchemy()


@pytest.fixture(scope="module")
def app_instance():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["DEBUG"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db.init_app(app)
    from .models import User, Role, Permission, RolePermission, Project, UserRole

    # Initialize the extension
    fsr = FlaskSecureRoles(app)

    # Define the routes
    @app.route("/role")
    @fsr.required_roles("hello", ["admin"])
    def roles_test():
        return "works"

    @app.route("/any-role")
    @fsr.any_role("hello", ["admin", "pop"])
    def any_roles_test():
        return "works"

    @app.route("/forbid-role")
    @fsr.forbid_roles("hello", ["admin"])
    def forbid_roles_test():
        return "works"

    @app.route("/mix-role")
    @fsr.forbid_roles("hello", ["admin"])
    @fsr.required_roles("hello", ["admin"])
    def mix_roles_test():
        return "works"

    return app


@pytest.fixture(scope="module")
def db_session(app_instance):
    with app_instance.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def client(app_instance: Flask):
    with app_instance.test_client() as client:
        yield client
