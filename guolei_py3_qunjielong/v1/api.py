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


class Api(object):
    """
    群接龙API Class
    """

    def __init__(
            self,
            base_url: str = "",
            secret: str = "",
            diskcache_cache: diskcache.Cache = None,
            redis_cache: Union[redis.Redis, redis.StrictRedis] = None,
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
        :param base_url:
        :param secret:
        :param diskcache_cache:
        :param redis_cache:
        """
        validate(instance=base_url, schema={"type": "string", "minLength": 1, "format": "uri", })
        validate(instance=secret, schema={"type": "string", "minLength": 1, })
        self._base_url = base_url
        self._secret = secret
        self._diskcache_cache = diskcache_cache
        self._redis_cache = redis_cache
        self._access_token = ""

    @property
    def base_url(self):
        return self._base_url

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
    def diskcache_cache(self):
        return self._diskcache_cache

    @diskcache_cache.setter
    def diskcache_cache(self, diskcache_cache):
        self._diskcache_cache = diskcache_cache

    @property
    def redis_cache(self):
        return self._redis_cache

    @redis_cache.setter
    def redis_cache(self, redis_cache):
        self._redis_cache = redis_cache

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    def query_home(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        获取主页信息(店铺信息)

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=09b80879-ddcb-49bf-b1e9-33181913924d
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/ghome/getGhomeInfo")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            },
                            "required": ["code", "success"],
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return None

    def query_access_token(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        获取访问凭证

        accessToken的存储需要至少256个字符空间。

        accessToken为全局唯一后台接口调用凭据，有效期为两个小时，重复获取会导致上一次接口返回的accessToken失效。
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/auth/token")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("secret", self.secret)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            },
                            "required": ["code", "success"],
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return None

    def access_token_with_diskcache_cache(
            self,
            diskcache_cache_key: str = None,
            diskcache_cache_expire: float = timedelta(minutes=110).total_seconds(),
            query_access_token_func_kwargs: dict = {},
    ):
        if not Draft202012Validator({"type": "number"}).is_valid(diskcache_cache_key):
            diskcache_cache_expire = timedelta(minutes=110).total_seconds()
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(query_access_token_func_kwargs, dict)):
            query_access_token_func_kwargs = {}
        query_access_token_func_kwargs = Dict(query_access_token_func_kwargs)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.diskcache_cache, diskcache.Cache)):
            if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(diskcache_cache_key):
                diskcache_cache_key = "_".join([
                    "guolei_py3_qunjielong_v1_api_diskcache_cache",
                    "access_token",
                    hashlib.md5(self.base_url.encode("utf-8")).hexdigest(),
                    hashlib.md5(self.secret.encode("utf-8")).hexdigest(),
                ])
            self.access_token = self.diskcache_cache.get(diskcache_cache_key)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.query_home(), NoneType)):
            self.access_token = self.query_access_token(**query_access_token_func_kwargs.to_dict())
            if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(self.access_token):
                self.diskcache_cache.set(
                    key=diskcache_cache_key,
                    value=self.access_token,
                    expire=diskcache_cache_expire
                )
        return self

    def access_token_with_redis_cache(
            self,
            redis_cache_key: str = None,
            redis_cache_expire: Union[int, timedelta] = timedelta(minutes=110),
            query_access_token_func_kwargs: dict = {},
    ):
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(query_access_token_func_kwargs, dict)):
            query_access_token_func_kwargs = {}
        query_access_token_func_kwargs = Dict(query_access_token_func_kwargs)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.redis_cache, (redis.Redis, redis.StrictRedis))):
            if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(redis_cache_key):
                diskcache_cache_key = "_".join([
                    "guolei_py3_qunjielong_v1_api_redis_cache",
                    "access_token",
                    hashlib.md5(self.base_url.encode("utf-8")).hexdigest(),
                    hashlib.md5(self.secret.encode("utf-8")).hexdigest(),
                ])
            self.access_token = self.redis_cache.get(redis_cache_key)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.query_home(), NoneType)):
            self.access_token = self.query_access_token(**query_access_token_func_kwargs.to_dict())
            if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(self.access_token):
                self.redis_cache.setex(
                    name=diskcache_cache_key,
                    value=self.access_token,
                    time=redis_cache_expire
                )
        return self

    def access_token_with_cache(
            self,
            cache_type: str = None,
            cache_key: str = None,
            cache_expire: Union[float, int, timedelta] = None,
            query_access_token_func_kwargs: dict = {},
    ):
        if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(cache_type):
            cache_type = "diskcache_cache"
        if cache_type.lower() not in ["diskcache_cache", "redis_cache"]:
            cache_type = "diskcache_cache"
        if cache_type.lower() == "diskcache_cache":
            return self.access_token_with_diskcache_cache(
                diskcache_cache_key=cache_key,
                diskcache_cache_expire=cache_expire,
                query_access_token_func_kwargs=query_access_token_func_kwargs
            )
        if cache_type.lower() == "redis_cache":
            return self.access_token_with_redis_cache(
                redis_cache_key=cache_key,
                redis_cache_expire=cache_expire,
                query_access_token_func_kwargs=query_access_token_func_kwargs
            )

        raise ValueError("Cache type must be 'diskcache_cache' or 'redis_cache'")

    def query_all_order_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        全量订单查询接口

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=a43156d1-2fa8-4ea6-9fb3-b550ceb7fe44

        全部状态订单查询 限流规则：接口每秒支持并发20次(QPS=20/S)。 请注意限制请求速度

        请求时间有一组必填即可：支付时间或更新时间

        相同参数请求最大请求大小为10000条。最大分页为第50页。
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/order/all/query_order_list")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_order_detail(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        订单详情查询接口

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=82385ad9-b3c5-4bcb-9e7a-2fbffd9fa69a

        限流规则：接口每秒支持并发20次(QPS=20/S)。 请注意限制请求速度
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/order/single/query_order_info")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_order_detail_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        批量获取订单详情接口

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=6d63014d-417a-4d16-8ba4-adffafe3b221

        限流规则：接口每秒支持并发20次(QPS=20/S)。 请注意限制请求速度
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/order/multi/query_order_info")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_goods_detail(
            self,
            goods_id="",
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        查询商品详情

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=000011fc-68ac-11eb-a95d-1c34da7b354c

        限流规则：接口每秒支持并发20次(QPS=20/S)。 请注意限制请求速度
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        validate(instance=goods_id, schema={
            "oneOf": [
                {"type": "integer", "minimum": 0},
                {"type": "string", "minLength": 1},
            ]
        })
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/goods/get_goods_detail/{goods_id}")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_goods_detail_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        批量查看商品详情接口

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=be50fc91-2cc7-490c-8b05-5789c4b966b8

        批量订单查询接口,最多支持50个商品
        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/goods/multi/get_goods_detail")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_act_goods_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        根据活动接龙号获取活动商品

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=55313bca-15ac-4c83-b7be-90e936829fe5

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/act_goods/query_act_goods")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_act_no_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        获取接龙号集合

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=3a9a0324-8345-464e-b8c1-ff9a40d3690d

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/act/query_actNo_list")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()

    def query_act_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        批量获取接龙信息

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=e1171d6b-49f2-4ff5-8bd6-5b87c8290460

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/open/api/act/list_act_info")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", {})
        request_func_kwargs.params.setdefault("accessToken", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "code": {
                                "oneOf": [
                                    {"type": "integer", "const": 200},
                                    {"type": "string", "const": "200"},
                                ]
                            },
                            "success": {
                                "type": "boolean",
                                "const": True,
                            }
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).data
        return Dict()
