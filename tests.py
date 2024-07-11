import os.path
import unittest

from diskcache import Cache

from guolei_py3_qunjielong import Api as QunjielongApi


class MyTestCase(unittest.TestCase):
    def test_something(self):
        qujielong_api = QunjielongApi(
            base_url="https://openapi.qunjielong.com",
            secret="2b318f774f5ffb82a2754cbb25a3ed33",
            diskcache=Cache(directory=os.path.join(os.path.dirname(__file__), "runtime", "database", "diskcache"))
        )
        act_goods=qujielong_api.access_token_with_cache().query_act_goods(act_no="2404110172842728")
        print(act_goods)
        self.assertTrue(True, 'test failed')  # add assertion here


if __name__ == '__main__':
    unittest.main()
