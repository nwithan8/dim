from functools import wraps

from dim.utils import _get_response_data


def raw_api_bool(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> bool:
        try:
            method = getattr(self._raw_api, func.__name__)
            return method(*args, **kwargs)
        except AttributeError:
            return False

    return wrapper


def get_json(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> dict:
        command, params = func(self, *args, **kwargs)
        if not command:
            return {}
        json_data = self._get_json(command=command, params=params)
        return _get_response_data(json_data=json_data)

    return wrapper


def post_json(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> dict:
        command, params = func(self, *args, **kwargs)
        if not command:
            return {}
        json_data = self._post_json(command=command, params=params)
        return _get_response_data(json_data=json_data)

    return wrapper


def post_bool(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> bool:
        command, params = func(self, *args, **kwargs)
        if not command:
            return False
        res = self._post(command=command, params=params)
        return res.ok

    return wrapper


def patch_json(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> dict:
        command, params = func(self, *args, **kwargs)
        if not command:
            return {}
        json_data = self._patch_json(command=command, params=params)
        return _get_response_data(json_data=json_data)

    return wrapper


def patch_bool(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> bool:
        command, params = func(self, *args, **kwargs)
        if not command:
            return False
        res = self._patch(command=command, params=params)
        return res.ok

    return wrapper


def delete_json(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> dict:
        command, params = func(self, *args, **kwargs)
        if not command:
            return {}
        json_data = self._delete_json(command=command, params=params)
        return _get_response_data(json_data=json_data)

    return wrapper


def delete_bool(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> bool:
        command, params = func(self, *args, **kwargs)
        if not command:
            return False
        res = self._delete(command=command, params=params)
        return res.ok

    return wrapper
