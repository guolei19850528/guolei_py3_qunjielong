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
import hashlib
from datetime import timedelta
from types import NoneType
from typing import Union, Callable

import diskcache
import redis
import requests
from addict import Dict
from jsonschema import validate
from jsonschema.validators import Draft202012Validator


class ApiUrlSettings:
    URL__OPEN__AUTH__TOKEN = "/open/auth/token"
    URL__OPEN__API__GHOME__GETGHOMEINFO = "/open/api/ghome/getGhomeInfo"
    URL__OPEN__API__GOODS__GET_GOODS_DETAIL = "/open/api/goods/get_goods_detail/"
    URL__OPEN__API__ORDER__ALL__QUERY_ORDER_LIST = "/open/api/order/all/query_order_list"
    URL__OPEN__API__ORDER__SINGLE__QUERY_ORDER_INFO = "/open/api/order/single/query_order_info"
    URL__OPEN__API__ACT__LIST_ACT_INFO = "/open/api/act/list_act_info"
    URL__OPEN__API__ACT_GOODS__QUERY_ACT_GOODS = "/open/api/act_goods/query_act_goods"


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

    def access_token(
            self,
            expire: Union[float | int | timedelta] = timedelta(seconds=7100).total_seconds(),
            custom_callable: Callable = None
    ):
        """
        access token
        :param expire: 过期时间
        :param custom_callable: 自定义回调 custom_callable(self) if isinstance(custom_callable, Callable)
        :return: custom_callable(self) if isinstance(custom_callable, Callable) else self
        """
        if isinstance(custom_callable, Callable):
            return custom_callable(self)
        validate(instance=self.base_url, schema={"type": "string", "minLength": 1, "pattern": "^http"})
        # 缓存key
        cache_key = f"guolei_py3_qunjielong_api_access_token__{self.secret}"
        # 使用缓存
        if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            if isinstance(self.cache_instance, diskcache.Cache):
                self._access_token = self.cache_instance.get(cache_key)
            if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                self._access_token = self.cache_instance.get(cache_key)
        # 用户是否登录
        response = requests.get(
            url=f"{self.base_url}{ApiUrlSettings.URL__OPEN__API__GHOME__GETGHOMEINFO}",
            params={
                "accessToken": self._access_token,
            },
            verify=False,
            timeout=(60, 60)
        )
        if response.status_code == 200:
            json_addict = response.json()
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "code": {
                        "oneOf": [
                            {"type": "integer", "const": 200},
                            {"type": "string", "const": "200"},
                        ]
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "ghId": {"type": "integer", "minimum": 1}
                        },
                        "required": ["ghId"]
                    }
                },
                "required": ["code", "data"]
            }).is_valid(json_addict):
                return self
        response = requests.get(
            url=f"{self.base_url}{ApiUrlSettings.URL__OPEN__AUTH__TOKEN}",
            params={
                "secret": self.secret,
            },
            verify=False,
            timeout=(60, 60)
        )
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "code": {
                        "oneOf": [
                            {"type": "integer", "const": 200},
                            {"type": "string", "const": "200"},
                        ]
                    },
                    "data": {"type": "string", "minLength": 1}
                },
                "required": ["code", "data"]
            }).is_valid(json_addict):
                self._access_token = json_addict.data
                # 缓存处理
                if isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
                    if isinstance(self.cache_instance, diskcache.Cache):
                        self.cache_instance.set(
                            key=cache_key,
                            value=self._access_token,
                            expire=expire
                        )
                    if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                        self.cache_instance.hset(
                            name=cache_key,
                            mapping=self._access_token
                        )
                        self.cache_instance.expire(
                            name=cache_key,
                            time=expire
                        )
        return self

    def get(
            self,
            url: str = "",
            params: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.get
        :param url: requests.get(url=url,params=params,**kwargs) url=base_url+url if not pattern ^http else url
        :param params: requests.get(url=url,params=params,**kwargs)
        :param kwargs: requests.get(url=url,params=params,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        params = Dict(params) if isinstance(params, dict) else Dict()
        params.setdefault("accessToken", self._access_token)
        response = requests.get(
            url=f"{url}",
            params=params,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "code": {
                        "oneOf": [
                            {"type": "integer", "const": 200},
                            {"type": "string", "const": "200"},
                        ],
                    },
                },
                "required": ["code", "data"]
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()

    def post(
            self,
            url: str = "",
            params: dict = None,
            data: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.post
        :param url: requests.post(url=url,params=params,data=data,**kwargs) url=base_url+url if not pattern ^http else url
        :param params: requests.post(url=url,params=params,data=data,**kwargs)
        :param data: requests.post(url=url,params=params,data=data,**kwargs)
        :param kwargs: requests.post(url=url,params=params,data=data,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        params = Dict(params) if isinstance(params, dict) else Dict()
        params.setdefault("accessToken", self._access_token)
        response = requests.post(
            url=url,
            params=params,
            data=data,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "code": {
                        "oneOf": [
                            {"type": "integer", "const": 200},
                            {"type": "string", "const": "200"},
                        ],
                    },
                },
                "required": ["code", "data"]
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()

    def put(
            self,
            url: str = "",
            data: dict = None,
            params: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.put
        :param url: requests.put(url=url,params=params,data=data,**kwargs) url=base_url+url if not pattern ^http else url
        :param params: requests.put(url=url,params=params,data=data,**kwargs)
        :param data: requests.put(url=url,params=params,data=data,**kwargs)
        :param kwargs: requests.put(url=url,params=params,data=data,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        params = Dict(params) if isinstance(params, dict) else Dict()
        params.setdefault("accessToken", self._access_token)
        response = requests.post(
            url=url,
            params=params,
            data=data,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "code": {
                        "oneOf": [
                            {"type": "integer", "const": 200},
                            {"type": "string", "const": "200"},
                        ],
                    },
                },
                "required": ["code", "data"]
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()

    def request(
            self,
            method: str = "GET",
            url: str = "",
            params: dict = None,
            data: dict = None,
            kwargs: dict = None,
            custom_callable: Callable = None
    ):
        """
        use requests.request
        :param method: requests.request(method=method,url=url,params=params,data=data,**kwargs)
        :param url: requests.request(method=method,url=url,params=params,data=data,**kwargs) url=base_url+url if not pattern ^http else url
        :param params: requests.request(method=method,url=url,params=params,data=data,**kwargs)
        :param data: requests.request(method=method,url=url,params=params,data=data,**kwargs)
        :param kwargs: requests.request(method=method,url=url,params=params,data=data,**kwargs)
        :param custom_callable: custom_callable(response) if isinstance(custom_callable,Callable)
        :return:custom_callable(response) if isinstance(custom_callable,Callable) else addict.Dict instance
        """
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        kwargs = Dict(kwargs) if isinstance(kwargs, dict) else Dict()
        params = Dict(params) if isinstance(params, dict) else Dict()
        params.setdefault("accessToken", self._access_token)
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            **kwargs.to_dict()
        )
        if isinstance(custom_callable, Callable):
            return custom_callable(response)
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if Draft202012Validator({
                "type": "object",
                "properties": {
                    "code": {
                        "oneOf": [
                            {"type": "integer", "const": 200},
                            {"type": "string", "const": "200"},
                        ],
                    },
                },
                "required": ["code", "data"]
            }).is_valid(json_addict):
                return json_addict.data
        return Dict()
