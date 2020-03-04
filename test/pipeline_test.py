import pandas
import pytest


@pytest.fixture
def hfd_pipeline():
    from src.main import main
    return main("/home/cole-work/PycharmProjects/hfd-spring-2020/test_data")


def test_hfd_pipeline(hfd_pipeline):
    assert hfd_pipeline()
