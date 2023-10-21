from flask_secure_roles.models import *
from .conftest import db 

class User(db.Model, UserMixin):
    __tablename__ = "User"

class Role(db.Model, RoleMixin):
    __tablename__ = "Role"

class Permission(db.Model, PermissionMixin):
    __tablename__ = "Permission"

class Project(db.Model, ProjectMixin):
    __tablename__ = "Project"

class UserRole(db.Model, UserRoleMixin):
    __tablename__ = "UserRole"

class RolePermission(db.Model, RolePermissionMixin):
    __tablename__ = "RolePermission"