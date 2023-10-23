import typing as t
from functools import wraps
from flask import Flask, jsonify, g, has_request_context, has_app_context
from werkzeug.local import LocalProxy
from .errors import MisconfigurationError
from .models import UserMixin

current_user = LocalProxy(lambda: _load_user())


def _load_user() -> t.Union[UserMixin, None]:
    if has_request_context() and has_app_context():
        if "_fsr_user" not in g:
            raise MisconfigurationError(
                "Either `user_loader` or `guest_user_loader` is not configured properly."
            )
        return g._fsr_user
    return None


class FlaskSecureRoles:
    _guest_loader = None

    def __init__(self, app: t.Union[Flask, None] = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.config.setdefault("FSR_TOKEN_LOCATION", "cookie")

        app.extensions["flask_secure_roles"] = self

    def user_loader(self, user: t.Union[UserMixin, None]) -> None:
        """
        Method to load the user from the user's authentication system.
        Sets the current_user for further usage

        :param user: FSR User model object of the user
        """
        if self._guest_loader is None:
            raise MisconfigurationError(
                "The `guest_user_loader` method is not implemented properly."
            )
        if user is None:
            user = self._guest_loader()
        if not issubclass(user.__class__, UserMixin):
            raise TypeError(
                "User must be an instance of a class derived from UserMixin"
            )
        g._fsr_user = user

    def guest_user_loader(self, callback: t.Callable) -> None:
        if callable(callback):
            self._guest_loader = callback
        else:
            raise TypeError(
                f"Expected callback to be a callable function or object, but received a {type(callback).__name__}."
            )

    def required_roles(self, project: str, roles: t.List[str]):
        """
        Allows the request only if the `current_user` has `roles` in current project
        :param str project: Project name to which the endpoint belongs to
        :param List[str] roles: List of roles which all are required
        """

        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # TODO: Implement the validation
                valid = False
                if valid:
                    return f(*args, **kwargs)
                else:
                    return jsonify(error="Unauthorized"), 401

            return decorated_function

        return decorator