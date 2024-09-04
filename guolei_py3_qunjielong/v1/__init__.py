#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
群接龙 Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_qunjielong
=================================================
"""
from typing import Union, Callable

import diskcache
import redis
import requests
from addict import Dict


class Api(object):
    """
    群接龙 第三方开放Api

    @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
    """

    def __init__(
            self,
            base_url: str = "",
            secret: str = "",
            diskcache_instance: diskcache.Cache = None,
            redis_instance: Union[redis.Redis, redis.StrictRedis] = None,
    ):
        self._base_url = base_url
        self._secret = secret
        self._diskcache_instance = diskcache_instance
        self._redis_instance = redis_instance

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, value):
        self._secret = value

    @property
    def diskcache_instance(self):
        return self._diskcache_instance

    @diskcache_instance.setter
    def diskcache_instance(self, value):
        self._diskcache_instance = value

    @property
    def redis_instance(self):
        return self._redis_instance

    @redis_instance.setter
    def redis_instance(self, value):
        self._redis_instance = value

    def open_auth_token(
            self,
            requests_request_func_kwargs_url_path: str = "/open/auth/token",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.params = {
            **{
                "secret": self.secret,
            },
            **requests_request_func_kwargs.params,
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.code == 200 and isinstance(json_addict.success, bool) and json_addict.success:
                return True, response.status_code, json_addict.data
        return False, response.status_code, Dict({})
