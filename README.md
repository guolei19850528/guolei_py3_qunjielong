from lxml.parser import result

# guolei-py3-qunjielong

### a python3 library for qunjielong

### [Document](https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/)
# Example

```python
import diskcache

from guolei_py3_qunjielong.library.api import (
    Api as QunjielongApi,
    UrlSetting as QunjielongApiUrlSetting
)

qunjielong_api: QunjielongApi = QunjielongApi(
    base_url="https://openapi.qunjielong.com/",
    secret="<YOUR SECRET>",
    cache_instance=diskcache.Cache()
)

result: dict = qunjielong_api.access_token().get(
    path=QunjielongApiUrlSetting.URL__OPEN__API__GHOME__GETGHOMEINFO
)

```