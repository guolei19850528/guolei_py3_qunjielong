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
        self._access_token = ""

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

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    def open_auth_token(
            self,
            requests_request_func_kwargs_url_path: str = "/open/auth/token",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        获取访问凭证

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=71e7934a-afce-4fd3-a897-e2248502cc94
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return:
        """
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
                self.access_token = json_addict.data
                return True, response, json_addict.data
        return False, response, response.json()

    def open_auth_token_with_diskcache(
            self,
            expire_time: float = timedelta(seconds=7000).total_seconds(),
            open_auth_token_func_kwargs: dict = {}
    ):
        if isinstance(self.diskcache_instance, diskcache.Cache):
            cache_key = "_".join([
                "guolei_py3_qunjielong",
                "v1",
                "Api",
                "diskcache",
                "access_token",
                f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
                f"{self.secret}",
            ])
            self.token_data = self.diskcache_instance.get(key=cache_key, default="")
            if not isinstance(self.token_data, str) or not len(self.token_data):
                request_response_state, _, _ = self.open_auth_token(**open_auth_token_func_kwargs)
                if request_response_state:
                    self.diskcache_instance.set(key=cache_key, value=self.access_token, expire=expire_time)
        else:
            self.open_auth_token(**open_auth_token_func_kwargs)
        return self

    def open_auth_token_with_redis(
            self,
            expire_time: Union[int, timedelta] = timedelta(seconds=7000),
            open_auth_token_func_kwargs: dict = {}
    ):
        if isinstance(self.redis_instance, (redis.Redis, redis.StrictRedis)):
            cache_key = "_".join([
                "guolei_py3_qunjielong",
                "v1",
                "Api",
                "redis",
                "access_token",
                f"{hashlib.md5(self.base_url.encode('utf-8')).hexdigest()}",
                f"{self.secret}",
            ])
            self.token_data = self.redis_instance.get(name=cache_key)
            if not isinstance(self.token_data, str) or not len(self.token_data):
                request_response_state, _, _ = self.open_auth_token(**open_auth_token_func_kwargs)
                if request_response_state:
                    self.redis_instance.setex(name=cache_key, value=self.access_token, time=expire_time)
        else:
            self.open_auth_token(**open_auth_token_func_kwargs)
        return self

    def open_api_order_all_query_order_list(
            self,
            requests_request_func_kwargs_json: dict = {},
            requests_request_func_kwargs_url_path: str = "/open/api/order/all/query_order_list",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        全量订单查询接口

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=a43156d1-2fa8-4ea6-9fb3-b550ceb7fe44
        :param requests_request_func_kwargs_json:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return:
        """
        requests_request_func_kwargs_json = Dict(requests_request_func_kwargs_json)
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "POST")
        requests_request_func_kwargs.params = {
            **{
                "accessToken": self.access_token,
            },
            **requests_request_func_kwargs.params,
        }
        requests_request_func_kwargs.json = {
            **requests_request_func_kwargs_json,
            **requests_request_func_kwargs.json,
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.code == 200 and isinstance(json_addict.success, bool) and json_addict.success:
                return True, response, json_addict.data
        return False, response, response.json()

    def open_api_order_single_query_order_info(
            self,
            order_no: str = "",
            requests_request_func_kwargs_url_path: str = "/open/api/order/single/query_order_info",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        订单详情查询接口

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=82385ad9-b3c5-4bcb-9e7a-2fbffd9fa69a
        :param requests_request_func_kwargs_json:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return:
        """
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "POST")
        requests_request_func_kwargs.params = {
            **{
                "accessToken": self.access_token,
            },
            **requests_request_func_kwargs.params,
        }
        requests_request_func_kwargs.json = {
            **{
                "orderNo": order_no,
            },
            **requests_request_func_kwargs.json,
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.code == 200 and isinstance(json_addict.success, bool) and json_addict.success:
                return True, response, json_addict.data
        return False, response, response.json()

    def open_api_act_goods_query_act_goods(
            self,
            act_no: str = "",
            requests_request_func_kwargs_url_path: str = "/open/api/act_goods/query_act_goods",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        根据活动接龙号获取活动商品

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=55313bca-15ac-4c83-b7be-90e936829fe5
        :param requests_request_func_kwargs_json:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return:
        """
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url", f"{self.base_url}{requests_request_func_kwargs_url_path}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.params = {
            **{
                "accessToken": self.access_token,
            },
            **requests_request_func_kwargs.params,
        }
        requests_request_func_kwargs.json = {
            **{
                "actNo": act_no,
            },
            **requests_request_func_kwargs.json,
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.code == 200 and isinstance(json_addict.success, bool) and json_addict.success:
                return True, response, json_addict.data
        return False, response, response.json()

    def open_api_act_goods_query_act_goods(
            self,
            goods_id: str = "",
            requests_request_func_kwargs_url_path: str = "open/api/goods/get_goods_detail",
            requests_request_func_kwargs: dict = {},
            requests_request_func_response_callable: Callable = None
    ):
        """
        查询商品详情

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=000011fc-68ac-11eb-a95d-1c34da7b354c
        :param requests_request_func_kwargs_json:
        :param requests_request_func_kwargs_url_path:
        :param requests_request_func_kwargs:
        :param requests_request_func_response_callable:
        :return:
        """
        requests_request_func_kwargs = Dict(requests_request_func_kwargs)
        requests_request_func_kwargs.setdefault("url",
                                                f"{self.base_url}{requests_request_func_kwargs_url_path}/{goods_id}")
        requests_request_func_kwargs.setdefault("method", "GET")
        requests_request_func_kwargs.params = {
            **{
                "accessToken": self.access_token,
            },
            **requests_request_func_kwargs.params,
        }
        response = requests.request(**requests_request_func_kwargs.to_dict())
        if isinstance(requests_request_func_response_callable, Callable):
            return requests_request_func_response_callable(response, requests_request_func_kwargs.to_dict())
        if response.status_code == 200:
            json_addict = Dict(response.json())
            if json_addict.code == 200 and isinstance(json_addict.success, bool) and json_addict.success:
                return True, response, json_addict.data
        return False, response, response.json()
