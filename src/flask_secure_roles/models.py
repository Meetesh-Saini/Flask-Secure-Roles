from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declared_attr
from .config import config

__all__ = [
    "UserMixin",
    "RoleMixin",
    "ProjectMixin",
    "PermissionMixin",
    "UserRoleMixin",
    "RolePermissionMixin",
]


class UserMixin:
    """
    Mixin for the `User` model
    """

    @declared_attr
    def fsr_user_id(cls):
        return Column(
            Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
        )

    @declared_attr
    def fsr_roles(cls):
        return relationship(
            config.fsr_models["userroleModel"], back_populates="fsr_user"
        )

    def user_id(self) -> str:
        """
        User ID of the user
        """
        return str(self.fsr_user_id)


class RoleMixin:
    """
    Mixin for the `Role` model
    """

    @declared_attr
    def fsr_role_id(cls):
        return Column(
            Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
        )

    @declared_attr
    def fsr_role_name(cls):
        return Column(String(256), nullable=False)

    @declared_attr
    def fsr_project_id(cls):
        return Column(
            Integer, ForeignKey(f"{config.fsr_tables['projectModel']}.fsr_project_id")
        )

    @declared_attr
    def fsr_project(cls):
        return relationship(
            config.fsr_models["projectModel"], back_populates="fsr_roles"
        )

    @declared_attr
    def fsr_users(cls):
        return relationship(
            config.fsr_models["userroleModel"], back_populates="fsr_role"
        )

    @declared_attr
    def fsr_permissions(cls):
        return relationship(
            config.fsr_models["rolepermissionModel"], back_populates="fsr_role"
        )

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint("fsr_role_name", "fsr_project_id"),)


    def name(self) -> str:
        return str(self.fsr_role_name)
    
class ProjectMixin:
    """
    Project Mixin for abstraction of various roles across various projects.
    """

    @declared_attr
    def fsr_project_id(cls):
        return Column(
            Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
        )

    @declared_attr
    def fsr_project_name(cls):
        return Column(String(256), unique=True, nullable=False)

    @declared_attr
    def fsr_roles(cls):
        return relationship(
            config.fsr_models["roleModel"], back_populates="fsr_project"
        )

    def name(self) -> str:
        """
        Returns the project name
        """
        return str(self.fsr_project_name)

class PermissionMixin:
    @declared_attr
    def fsr_permission_id(cls):
        return Column(
            Integer, autoincrement=True, primary_key=True, unique=True, nullable=False
        )

    @declared_attr
    def fsr_permission_name(cls):
        return Column(String(256), nullable=False)

    @declared_attr
    def fsr_roles(cls):
        return relationship(
            config.fsr_models["rolepermissionModel"], back_populates="fsr_permission"
        )

    def name(self) -> str:
        return str(self.fsr_permission_name)

class UserRoleMixin:
    @declared_attr
    def fsr_role_id(cls):
        return Column(
            Integer,
            ForeignKey(f"{config.fsr_tables['roleModel']}.fsr_role_id"),
            primary_key=True,
        )

    @declared_attr
    def fsr_user_id(cls):
        return Column(
            Integer,
            ForeignKey(f"{config.fsr_tables['userModel']}.fsr_user_id"),
            primary_key=True,
        )

    @declared_attr
    def fsr_user(cls):
        return relationship(config.fsr_models["userModel"], back_populates="fsr_roles")

    @declared_attr
    def fsr_role(cls):
        return relationship(config.fsr_models["roleModel"], back_populates="fsr_users")


class RolePermissionMixin:
    @declared_attr
    def fsr_role_id(cls):
        return Column(
            Integer,
            ForeignKey(f"{config.fsr_tables['roleModel']}.fsr_role_id"),
            primary_key=True,
        )

    @declared_attr
    def fsr_permission_id(cls):
        return Column(
            Integer,
            ForeignKey(f"{config.fsr_tables['permissionModel']}.fsr_permission_id"),
            primary_key=True,
        )

    @declared_attr
    def fsr_role(cls):
        return relationship(
            config.fsr_models["roleModel"], back_populates="fsr_permissions"
        )

    @declared_attr
    def fsr_permission(cls):
        return relationship(
            config.fsr_models["permissionModel"], back_populates="fsr_roles"
        )
