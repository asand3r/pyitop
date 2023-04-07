import time
import json
import requests

from typing import Union


class ItopAPIException(Exception):
    pass


class ItopAPI:
    total_requests = 0

    def __init__(self, url: str, user: str, password: str, ssl_verify: bool = False):
        self.url = url
        self.__user = user
        self.__password = password
        self.ssl_verify = ssl_verify

    @property
    def user(self) -> str:
        return self.__user

    @user.setter
    def user(self, value: str):
        self.__user = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value

    def get(self, class_: str, key: Union[str, dict[str, str]] = "*", output: list = None) -> list:
        self.total_requests += 1
        key = {} if key == "*" else key
        if not isinstance(output, (list, type(None))):
            raise ValueError("output_fields must be a list or None to get all fields")

        output_fields = "*" if output is None else ",".join([i.strip() for i in output])
        req_body = {'operation': 'core/get', 'class': class_, 'key': key, 'output_fields': output_fields}
        req_data = {'auth_user': self.user, 'auth_pwd': self.password, 'json_data': json.dumps(req_body)}
        resp_raw = requests.post(self.url, verify=self.ssl_verify, data=req_data)
        if not resp_raw.status_code == 200:
            return []

        resp_json = resp_raw.json()
        if not resp_json['code']:
            return [v for v in resp_json['objects'].values()] if resp_json['objects'] else []
        else:
            raise ItopAPIException(resp_json['message'])

    def update(self, class_: str, key: str, fields: dict) -> dict:
        self.total_requests += 1
        time_format = '%Y.%m.%d %H:%M:%S %z'
        req_body = {'operation': 'core/update', 'class': class_, 'key': key, 'output_fields': 'name'}
        req_body = req_body | {'comment': f'itop2zbx: {time.strftime(time_format, time.localtime())}', 'fields': fields}
        req_data = {'auth_user': self.user, 'auth_pwd': self.password, 'json_data': json.dumps(req_body)}
        resp_raw = requests.post(self.url, verify=self.ssl_verify, data=req_data)
        if not resp_raw.status_code == 200:
            return {}

        resp_json = resp_raw.json()
        if not resp_json['code']:
            return resp_json['objects'] if resp_json['objects'] else {}
        else:
            raise ItopAPIException(resp_json['message'])
