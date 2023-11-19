import pytest
import orjson
from pathlib import Path
from st2dl.download.preview import get_preview_download_links


@pytest.fixture()
def search_result():
    with open(Path(__file__).parent / "data" / "test_search_data.json", "rb") as f:
        data = orjson.loads(f.read())
    return data


def test_preview_links(search_result):
    preview_links = get_preview_download_links(search_result)

    assert [i["url"] for i in preview_links] == [
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(a7aa6a3c-4c4a-4a50-be49-fe874669dbc6)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(fb43fe4d-a795-4726-ae1a-cdd02376a414)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(6d5ae0d3-4989-4e0e-9f13-7cd8012bdaf2)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(1beb9210-c427-4112-9e1e-b9abf2019e88)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(ba2e261a-be34-495e-b4c6-19453f358bc0)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(e35a2cec-ef70-4512-8665-38db9e6da685)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(f9b050c4-670c-4e8f-bc47-7c81d1546bf1)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(67c98856-1ceb-4988-ac72-a2e0cca9d22e)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(4c96f24b-09c2-4b11-b5cc-be516101b389)/$value",
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Assets(e4d159dd-904b-468f-9b47-67a09dc7794c)/$value",
    ]
