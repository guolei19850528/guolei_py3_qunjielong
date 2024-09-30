#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_qunjielong
=================================================
"""
from datetime import timedelta
from typing import Union, Callable, Any

import diskcache
import redis
import requests
from addict import Dict
from guolei_py3_requests.library import ResponseCallable, request
from jsonschema import validate
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallable(object):
    """
    Response Callable Class
    """

    @staticmethod
    def json_code_200(response: Response = None, status_code: int = 200):
        json_data = response.json() if response.status_code == status_code else dict()
        if int(json_data.get("code", -1)) == 200:
            return json_data.get("data",dict)
        return None


class UrlSetting(object):
    OPEN__AUTH__TOKEN = "/open/auth/token"
    OPEN__API__GHOME__GETGHOMEINFO = "/open/api/ghome/getGhomeInfo"
    OPEN__API__GOODS__GET_GOODS_DETAIL = "/open/api/goods/get_goods_detail/"
    OPEN__API__ORDER__ALL__QUERY_ORDER_LIST = "/open/api/order/all/query_order_list"
    OPEN__API__ORDER__SINGLE__QUERY_ORDER_INFO = "/open/api/order/single/query_order_info"
    OPEN__API__ACT__LIST_ACT_INFO = "/open/api/act/list_act_info"
    OPEN__API__ACT_GOODS__QUERY_ACT_GOODS = "/open/api/act_goods/query_act_goods"


class Api(object):
    """
    @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
    """

    def __init__(
            self,
            base_url: str = "https://openapi.qunjielong.com/",
            secret: str = "",
            cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        self._base_url = base_url
        self._secret = secret
        self._cache_instance = cache_instance
        self._access_token = ""

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, secret):
        self._secret = secret

    @property
    def cache_instance(self):
        return self._cache_instance

    @cache_instance.setter
    def cache_instance(self, cache_instance):
        self._cache_instance = cache_instance

    def get_access_token_by_cache(self, name: str = None):
        name = name or f"guolei_py3_qunjielong_api_access_token__{self.secret}"
        if isinstance(self.cache_instance, diskcache.Cache):
            self._access_token = self.cache_instance.get(name)
        if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
            self._access_token = self.cache_instance.get(name)
        return self._access_token or ""

    def put_access_token_to_cache(
            self,
            name: str = None,
            expire: Union[float, int, timedelta] = None,
            access_token: str = None
    ):
        name = name or f"guolei_py3_qunjielong_api_access_token__{self.secret}"
        access_token = access_token or self._access_token
        if isinstance(self.cache_instance, diskcache.Cache):
            return self.cache_instance.set(
                key=name,
                value=access_token,
                expire=expire or timedelta(seconds=7100).total_seconds()
            )
        if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
            self.cache_instance.setex(
                name=name,
                value=access_token,
                time=expire or timedelta(seconds=7100),
            )
            return True
        return False

    def get(self, on_response_callback: Callable = ResponseCallable.json_code_200, path: str = None, **kwargs):
        """
        execute get by requests.get

        params.setdefault("accessToken", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("accessToken", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.get(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def post(self, on_response_callback: Callable = ResponseCallable.json_code_200, path: str = None, **kwargs):
        """
        execute post by requests.post

        params.setdefault("accessToken", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("accessToken", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.post(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def put(self, on_response_callback: Callable = ResponseCallable.json_code_200, path: str = None, **kwargs):
        """
        execute put by requests.put

        params.setdefault("accessToken", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("accessToken", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.put(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def request(self, on_response_callback: Callable = ResponseCallable.json_code_200, path: str = None,
                **kwargs):
        """
        execute request by requests.request

        params.setdefault("accessToken", self._access_token)

        :param on_response_callback: response callback
        :param path: if url is None: url=f"{self.base_url}{path}"
        :param kwargs: requests.get(**kwargs)
        :return: on_response_callback(response) or response
        """
        path = kwargs.get("url", None) or f"{self.base_url}{path}"
        params = kwargs.get("params", dict())
        params.setdefault("accessToken", self._access_token)
        kwargs.update([
            ("params", params),
            ("url", path),
        ])
        response = requests.request(**kwargs)
        if isinstance(on_response_callback, Callable):
            return on_response_callback(response)
        return response

    def access_token(self):
        """
        access token
        :return:
        """
        self._access_token = self.get_access_token_by_cache()
        result = self.get(
            path=f"{UrlSetting.OPEN__API__GHOME__GETGHOMEINFO}",
            verify=False,
            timeout=(60, 60)
        )
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "ghId": {"type": "integer", "minimum": 1},
            },
            "required": ["ghId"]
        }).is_valid(result):
            return self
        result = self.get(
            path=f"{UrlSetting.OPEN__AUTH__TOKEN}",
            params={
                "secret": self.secret,
            },
            verify=False,
            timeout=(60, 60)
        )
        if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(result):
            self._access_token = result
        return self
