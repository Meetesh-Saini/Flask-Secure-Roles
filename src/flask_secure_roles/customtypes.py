import typing as t

ModelsDict = t.Dict[
    t.Literal[
        "userModel",
        "projectModel",
        "roleModel",
        "permissionModel",
        "userroleModel",
        "rolepermissionModel",
    ],
    str,
]
