from __future__ import annotations
import typing as t
from .customtypes import *

from flask import current_app


class _Config:
    """
    Config class for storing the default configurations of the app
    """

    # Default class names for the models
    _userModel = "User"
    _projectModel = "Project"
    _roleModel = "Role"
    _permissionModel = "Permission"
    _userroleModel = "UserRole"
    _rolepermissionModel = "RolePermission"

    # Default table names for the models
    _userTablename = "User"
    _projectTablename = "Project"
    _roleTablename = "Role"
    _permissionTablename = "Permission"
    _userroleTablename = "UserRole"
    _rolepermissionTablename = "RolePermission"

    @property
    def token_location(self) -> t.Literal["cookie"]:
        """
        Specifies the location of the access token and the refresh token

        :return: The location of the tokens. Default is "cookie".
        :rtype: str

        .. note::
            The default value is "cookie".
        """
        return current_app.config.get("FSR_TOKEN_LOCATION", "cookie")

    @property
    def fsr_models(
        self,
    ) -> ModelsDict:
        return {
            "userModel": self._userModel,
            "projectModel": self._projectModel,
            "roleModel": self._roleModel,
            "permissionModel": self._permissionModel,
            "userroleModel": self._userroleModel,
            "rolepermissionModel": self._rolepermissionModel,
        }

    @fsr_models.setter
    def fsr_models(
        self,
        userModel: str,
        projectModel: str,
        roleModel: str,
        permissionModel: str,
        userroleModel: str,
        rolepermissionModel: str,
    ) -> None:
        if (
            userModel is None
            or projectModel is None
            or roleModel is None
            or permissionModel is None
            or userroleModel is None
            or rolepermissionModel is None
        ):
            raise ValueError("Insufficient model names: All models are required")
        self._userModel = userModel
        self._projectModel = projectModel
        self._roleModel = roleModel
        self._permissionModel = permissionModel
        self._userroleModel = userroleModel
        self._rolepermissionModel = rolepermissionModel

    @property
    def fsr_tables(self) -> ModelsDict:
        return {
            "userModel": self._userTablename,
            "projectModel": self._projectTablename,
            "roleModel": self._roleTablename,
            "permissionModel": self._permissionTablename,
            "userroleModel": self._userroleTablename,
            "rolepermissionModel": self._rolepermissionTablename,
        }

    @fsr_tables.setter
    def fsr_tables(
        self,
        userTablename: str,
        projectTablename: str,
        roleTablename: str,
        permissionTablename: str,
        userroleTablename: str,
        rolepermissionTablename: str,
    ) -> None:
        if (
            userTablename is None
            or projectTablename is None
            or roleTablename is None
            or permissionTablename is None
            or userroleTablename is None
            or rolepermissionTablename is None
        ):
            raise ValueError("Insufficient model names: All models are required")
        self._userTablename = userTablename
        self._projectTablename = projectTablename
        self._roleTablename = roleTablename
        self._permissionTablename = permissionTablename
        self._userroleTablename = userroleTablename
        self._rolepermissionTablename = rolepermissionTablename


config = _Config()
