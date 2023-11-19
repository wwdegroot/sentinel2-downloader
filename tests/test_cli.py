import pytest

from st2dl.cli import wkt_to_point, convert_to_timestamp
from st2dl.exceptions import InvalidWktPointArgument


def test_valid_wkt_to_point():
    long, lat = wkt_to_point("POINT(-9.1372 38.7000)")
    assert lat == 38.7000
    assert long == -9.1372


def test_invalid_wkt_to_point():
    with pytest.raises(InvalidWktPointArgument):
        wkt_to_point("LINESTRING(-9.1372 38.7000, -9.1372 39.7000 )")


def test_convert_to_timestamp():
    date_without_hours = "21-8-2023"
    date_with_hours = "21-8-2023 00:00:00"
    esa_date_without_hours = convert_to_timestamp(date_without_hours)
    esa_date_with_hours = convert_to_timestamp(date_with_hours)
    assert esa_date_without_hours == "2023-08-21T00:00:00.000000Z"
    assert esa_date_with_hours == "2023-08-21T00:00:00.000000Z"
