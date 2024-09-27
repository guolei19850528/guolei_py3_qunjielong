from lxml.parser import result

# guolei-py3-qunjielong

### a python3 library for qunjielong

### [Document](https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/)
# Example

```python
import diskcache

diskcache_default_instance = diskcache.Cache()

from guolei_py3_qunjielong.library.api import (
    Api as QunjielongApi,
    ApiUrlSettings as QunjielongApiUrlSettings
)

qunjielong_api: QunjielongApi = QunjielongApi(
    base_url="https://openapi.qunjielong.com/",
    secret="<YOUR SECRET>",
    cache_instance=diskcache_default_instance
)

result: dict = qunjielong_api.access_token().get(
    url=QunjielongApiUrlSettings.URL__OPEN__API__GHOME__GETGHOMEINFO
)

```