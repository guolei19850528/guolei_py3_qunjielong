# guolei_py3_qunjielong

## introduce

**guolei python3 qunjielong library**

## software architecture

~python 3.*

## installation tutorial

```shell
pip install guolei-py3-qunjielong
```

## catalog description
### Qujielong Api Example
```python

# @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/

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