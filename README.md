## 介绍

**群接龙 API**

[官方文档](https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/)

## 软件架构

~python 3.*

## 安装教程

```shell
pip install guolei-py3-qunjielong
```

## 目录说明

### Qujielong Api 示例

```python

from diskcache import Cache

from guolei_py3_qunjielong import Api as QunjielongApi

qujielong_api = QunjielongApi(
    base_url="https://openapi.qunjielong.com",
    secret="secret",
    diskcache=Cache()
)
act_goods = qujielong_api.access_token_with_cache().query_act_goods(act_no="2404110172842728")
print(act_goods)
```