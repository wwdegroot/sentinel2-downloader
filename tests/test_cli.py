import pytest

from st2dl.cli import wkt_to_point
from st2dl.exceptions import InvalidWktPointArgument


def test_valid_wkt_to_point():
    long, lat = wkt_to_point("POINT(-9.1372 38.7000)")
    assert lat == 38.7000
    assert long == -9.1372


def test_invalid_wkt_to_point():
    with pytest.raises(InvalidWktPointArgument):
        wkt_to_point("LINESTRING(-9.1372 38.7000, -9.1372 39.7000 )")
