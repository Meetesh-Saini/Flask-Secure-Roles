# tests/test_mixins.py
from .models import User, Role, Project, Permission, RolePermission, UserRole
from sqlalchemy.orm import scoped_session, Session


def test_usermixin_user_id(db_session: scoped_session[Session]):
    # Create a UserMixin instance
    user = User()

    # Add user to the session
    db_session.add(user)
    db_session.commit()

    # Retrieve user from the session
    retrieved_user = db_session.query(User).first()

    # Test the user_id method
    assert retrieved_user.user_id() == str(retrieved_user.fsr_user_id)

    # Removing the user
    db_session.delete(user)
    db_session.commit()


def test_usermixin_many_user_id(db_session: scoped_session[Session]):
    # Create a UserMixin instance
    user1 = User()
    user2 = User()
    # Add user to the session
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    # Retrieve user from the session
    retrieved_user = db_session.query(User)

    # Test the user_id method
    uid = 1
    for user in retrieved_user:
        assert user.user_id() == str(uid)
        uid += 1

    # Removing the users
    db_session.delete(user1)
    db_session.delete(user2)
    db_session.commit()


def test_usermixin_custom_user_id(db_session: scoped_session[Session]):
    user = User(fsr_user_id=4)
    db_session.add(user)
    db_session.commit()

    retrieved_user = db_session.query(User).first()

    assert retrieved_user.user_id() == user.user_id()

    # Removing the user
    db_session.delete(user)
    db_session.commit()


def test_projectmixin(db_session: scoped_session[Session]):
    projectname = "hello"
    rolename = "myrole"
    permissonname = "edit-blog"

    # Create a user and project
    user = User()
    project = Project(fsr_project_name=projectname)

    db_session.add(user)
    db_session.add(project)
    db_session.commit()

    # Retrive the user and project
    retrieved_user = db_session.query(User).first()
    retrieved_project: Project = db_session.query(Project).first()

    assert retrieved_project.name() == projectname

    # Create the role and permission
    role = Role(fsr_role_name=rolename, fsr_project_id=retrieved_project.fsr_project_id)
    permisson = Permission(fsr_permission_name=permissonname)

    db_session.add(role)
    db_session.add(permisson)
    db_session.commit()

    retrieved_role: Role = db_session.query(Role).first()
    retrieved_permission: Permission = db_session.query(Permission).first()

    assert retrieved_role.name() == rolename
    assert retrieved_role.fsr_project_id == retrieved_project.fsr_project_id

    assert retrieved_permission.name() == permissonname

    # Map roles and permissions
    role_mapped = RolePermission(
        fsr_role_id=retrieved_role.fsr_role_id,
        fsr_permission_id=retrieved_permission.fsr_permission_id,
    )

    db_session.add(role_mapped)
    db_session.commit()

    retrieved_rolepermission: RolePermission = db_session.query(RolePermission).first()

    assert retrieved_rolepermission.fsr_role_id == retrieved_role.fsr_role_id
    assert (
        retrieved_rolepermission.fsr_permission_id
        == retrieved_permission.fsr_permission_id
    )
    assert retrieved_rolepermission.fsr_permission.name() == permissonname
    assert retrieved_rolepermission.fsr_role.name() == rolename

    # Map the user to the role
    user_mapped = UserRole(
        fsr_user_id=retrieved_user.fsr_user_id, fsr_role_id=retrieved_role.fsr_role_id
    )

    db_session.add(user_mapped)
    db_session.commit()

    retrieved_userrole: UserRole = db_session.query(UserRole).first()

    assert retrieved_userrole.fsr_role.name() == rolename
    assert retrieved_userrole.fsr_role.fsr_project_id == retrieved_project.fsr_project_id
