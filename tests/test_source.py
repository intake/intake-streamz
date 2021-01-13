import os
import pytest
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


def test_dask():
    distr = pytest.importorskip("dask.distributed")
    import streamz.dask
    with distr.Client():
        cat = intake.open_catalog(catfile)
        s = cat.simple.to_dask()
        assert isinstance(s, streamz.dask.DaskStream)
        l = s.gather().sink_to_list()
        s.start()
        wait_for(lambda: l == [1, 2, 3], timeout=1)


def test_df():
    dataframe = pytest.importorskip("streamz.dataframe")
    cat = intake.open_catalog(catfile)
    s = cat.df.read()
    assert isinstance(s, dataframe.DataFrame)
    s.start()
    wait_for(lambda: s.current_value is not None, timeout=1)
    cv = s.current_value
    wait_for(lambda: not s.current_value.equals(cv), timeout=1)


def test_plot():
    pytest.importorskip("streamz.dataframe")
    pytest.importorskip("hvplot")
    cat = intake.open_catalog(catfile)
    s = cat.df.read()
    pl = s.plot()
    assert "DynamicMap" in str(pl)
