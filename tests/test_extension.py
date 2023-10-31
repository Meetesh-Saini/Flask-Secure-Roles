from flask_secure_roles import FlaskSecureRoles, current_user
from flask_secure_roles.errors import MisconfigurationError
from flask import Flask
from flask.testing import FlaskClient
import pytest
from sqlalchemy.orm import scoped_session, Session
from .models import db, User, Project, Role, UserRole


def test_extension_load(app_instance: Flask):
    fsr = FlaskSecureRoles(app_instance)

    assert "flask_secure_roles" in app_instance.extensions


def test_extension_current_user(
    app_instance: Flask, client: FlaskClient, db_session: scoped_session[Session]
):
    # Remove all of the changes done by other tests
    db_session.expunge_all()

    # Initialize the extension
    fsr = FlaskSecureRoles(app_instance)

    assert current_user == None

    # Define the route
    @app_instance.route("/")
    def home():
        return current_user._get_current_object().user_id()

    # Test if misconfiguration is there
    with pytest.raises(
        MisconfigurationError,
        match="Either `user_loader` or `guest_user_loader` is not configured properly.",
    ):
        resp = client.get("/")

    # Define the `guest_user_loader` but incorrectly
    @fsr.guest_user_loader
    def guest_loader():
        return "hi"

    # Test if the `guest_user_loader` is returning a derivative of UserMixin
    with pytest.raises(
        TypeError, match="User must be an instance of a class derived from UserMixin"
    ):
        fsr.user_loader(None)

    # Create a guest user
    user = User(name="guest")
    user2 = User(name="john")
    # Add user to the session
    db_session.add(user)
    db_session.add(user2)
    db_session.commit()

    # Retrieve the users
    guest_user = db_session.query(User).filter(User.name == "guest").first()
    real_user = db_session.query(User).filter(User.name == "john").first()

    # Configure the `guest_user_loader` properly
    @fsr.guest_user_loader
    def guest_loader():
        return guest_user

    # Set the user to None to use guest user
    fsr.user_loader(None)

    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == guest_user.user_id()

    # Set the user to john
    fsr.user_loader(real_user)

    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == real_user.user_id()


def test_required_roles(
    app_instance: Flask, client: FlaskClient, db_session: scoped_session[Session]
):
    real_user = db_session.query(User).filter(User.name == "john").first()
    fsr = app_instance.extensions["flask_secure_roles"]
    # Set the user to john
    fsr.user_loader(real_user)
    resp = client.get("/role")

    assert resp.status_code == 401

    # Create the project
    project = Project(fsr_project_name="hello")
    db_session.add(project)
    db_session.commit()
    project: Project = (
        db_session.query(Project).filter(Project.fsr_project_name == "hello").first()
    )

    # Create the role
    role = Role(fsr_role_name="admin", fsr_project_id=project.fsr_project_id)
    db_session.add(role)
    db_session.commit()
    role: Role = db_session.query(Role).filter(Role.fsr_role_name == "admin").first()

    # Map user to role
    userrole = UserRole(fsr_user_id=real_user.fsr_user_id, fsr_role_id=role.fsr_role_id)
    db_session.add(userrole)
    db_session.commit()

    # Visit the route
    resp = client.get("/role")

    assert resp.status_code == 200
    assert resp.data == b"works"
