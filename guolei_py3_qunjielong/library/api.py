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
from addict import Dict
from guolei_py3_requests.library import ResponseCallable, request
from jsonschema import validate
from jsonschema.validators import Draft202012Validator
from requests import Response


class ResponseCallable(ResponseCallable):
    """
    Response Callable Class
    """

    @staticmethod
    def json_addict__code_is_200(response: Response = None, status_code: int = 200):
        json_addict = ResponseCallable.json_addict(response=response, status_code=status_code)
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


class UrlsSetting:
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

    def access_token(
            self,
            expire: Union[float | int | timedelta] = timedelta(seconds=7100).total_seconds(),
            access_token_callable: Callable = None
    ):
        """
        access token
        :param expire: 过期时间
        :param access_token_callable: 自定义回调 custom_callable(self) if isinstance(custom_callable, Callable)
        :return: custom_callable(self) if isinstance(custom_callable, Callable) else self
        """
        if isinstance(access_token_callable, Callable):
            return access_token_callable(self)
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
        result = self.get(
            is_with_access_token=True,
            url=f"{self.base_url}{UrlsSetting.OPEN__API__GHOME__GETGHOMEINFO}",
            verify=False,
            timeout=(60, 60)
        )
        if Draft202012Validator({
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "properties": {
                        "ghId": {"type": "integer", "minimum": 1}
                    },
                    "required": ["ghId"]
                }
            },
            "required": ["data"]
        }).is_valid(result):
            return self

        result = self.get(
            is_with_access_token=False,
            url=f"{self.base_url}{UrlsSetting.OPEN__AUTH__TOKEN}",
            params={
                "secret": self.secret,
            },
            verify=False,
            timeout=(60, 60)
        )

        if Draft202012Validator({
            "type": "string",
            "properties": {
                "data": {"type": "string", "minLength": 1}
            },
            "required": ["data"]
        }).is_valid(result):
            self._access_token = result
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
            is_with_access_token=True,
            response_callable: Callable = ResponseCallable.json_addict__code_is_200,
            url: str = None,
            params: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        return self.request(
            is_with_access_token=is_with_access_token,
            response_callable=response_callable,
            method="GET",
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )

    def post(
            self,
            is_with_access_token=True,
            response_callable: Callable = ResponseCallable.json_addict__code_is_200,
            url: str = None,
            params: Any = None,
            data: Any = None,
            json: Any = None,
            headers: Any = None,
            **kwargs: Any
    ):
        return self.request(
            is_with_access_token=is_with_access_token,
            response_callable=response_callable,
            method="POST",
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            **kwargs
        )

    def request(
            self,
            is_with_access_token=True,
            response_callable: Callable = ResponseCallable.json_addict__code_is_200,
            method: str = "GET",
            url: str = None,
            params: Any = None,
            headers: Any = None,
            **kwargs
    ):
        if not Draft202012Validator({"type": "string", "minLength": 1, "pattern": "^http"}).is_valid(url):
            url = f"/{url}" if not url.startswith("/") else url
            url = f"{self.base_url}{url}"
        params = Dict(params) if isinstance(params, dict) else Dict()
        if is_with_access_token:
            params.setdefault("access_token", self._access_token)
        return request(
            response_callable=response_callable,
            method=method,
            url=url,
            params=params,
            headers=headers,
            **kwargs
        )
