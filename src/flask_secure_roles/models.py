import typing as t
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

    def roles(self, project_id=None, project_name=None) -> t.List[str]:
        """
        Roles of the user in the project with id `project_id`

        :param project_id: Project ID of the project whose roles are needed
        :param project_name: Project name whose roles are needed
        :return: List of the roles
        :rtype: List[str]
        """
        roles_list = []
        if project_id is None and project_name is None:
            for user_role in self.fsr_roles:
                roles_list.append(str(user_role.fsr_role.name()))
        elif project_id is not None:
            for user_role in self.fsr_roles:
                if user_role.fsr_role.fsr_project_id == project_id:
                    roles_list.append(str(user_role.fsr_role.name()))
        elif project_name is not None:
            for user_role in self.fsr_roles:
                if user_role.fsr_role.fsr_project.name() == project_name:
                    roles_list.append(str(user_role.fsr_role.name()))
        return roles_list


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

    def has_permission(self, project_name, permission_name) -> bool:
        """
        Checks if the role has `permission_name` permission in `project_name` project

        :param project_name: Project name
        :param permission_name: Permission name
        :return: `True` if the role has permission in the project otherwise `False`
        :rtype: bool
        """
        if self.fsr_project.fsr_project_name != project_name:
            return False
        for permission in self.fsr_permissions:
            if permission.fsr_permission.name() == permission_name:
                return True
        return False


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
