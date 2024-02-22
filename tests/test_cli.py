import pytest

from st2dl.cli import wkt_to_point, convert_to_timestamp, daterange_to_timestamp
from st2dl.exceptions import InvalidWktPointArgument, InvalidDateRangeArgument


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


def test_daterange_valid():
    daterange_without_hours = "21-8-2023,21-9-2023"
    time_gt, time_lt = daterange_to_timestamp(daterange_without_hours)
    assert time_gt == "2023-08-21T00:00:00.000000Z"
    assert time_lt == "2023-09-21T00:00:00.000000Z"


def test_daterange_missing_comma():
    invalid_daterange = "21-8-2023"
    with pytest.raises(InvalidDateRangeArgument) as drexc:
        daterange_to_timestamp(invalid_daterange)
    assert (
        str(drexc.value)
        == f'Give a valid daterange string. for example: "11-08-2023 00:00:00,11-09-2023 00:00:00" \n Daterange received: {invalid_daterange}'
    )


def test_daterange_invalid_gt_format():
    invalid_daterange_gt = "211-8-2023,22-10-2023"
    with pytest.raises(InvalidDateRangeArgument) as drexc:
        daterange_to_timestamp(invalid_daterange_gt)
    assert (
        str(drexc.value)
        == "Invalid dateformat encountered for time_gt: 211-8-2023. Dateformat expected: %d-%m-%Y or %d-%m-%Y %H:%M:%S"
    )


def test_daterange_invalid_lt_format():
    invalid_daterange_lt = "21-8-2023,222-10-2023"
    with pytest.raises(InvalidDateRangeArgument) as drexc:
        daterange_to_timestamp(invalid_daterange_lt)
    assert (
        str(drexc.value)
        == "Invalid dateformat encountered for time_lt: 222-10-2023. Dateformat expected: %d-%m-%Y or %d-%m-%Y %H:%M:%S"
    )
