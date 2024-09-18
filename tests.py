import os.path
import unittest

from diskcache import Cache

from guolei_py3_qunjielong.v1.api import Api as QunjielongApi

diskcache_cache_default = Cache(directory=os.path.join(os.path.dirname(__file__), "runtime", "database", "diskcache"))


class MyTestCase(unittest.TestCase):
    def test_something(self):
        qujielong_api = QunjielongApi(
            base_url="https://openapi.qunjielong.com",
            secret="",
            diskcache_cache=diskcache_cache_default
        )
        self.assertTrue(True, 'test failed')  # add assertion here


if __name__ == '__main__':
    unittest.main()
