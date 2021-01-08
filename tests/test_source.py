import os
import intake
from streamz.utils_test import wait_for

catfile = os.path.join(os.path.dirname(__file__), "catalog.yaml")


def test_simple():
    cat = intake.open_catalog(catfile)
    s = cat.simple.read()
    l = s.sink_to_list()
    assert not l
    s.start()
    wait_for(lambda: l == [1, 2, 3], timeout=1)
