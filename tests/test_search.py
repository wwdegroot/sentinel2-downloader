import json
from pathlib import Path

import pytest
from pytest_httpx import HTTPXMock
from st2dl.download.search import search_odata, SearchContent


@pytest.mark.asyncio
async def test_search_odata(httpx_mock: HTTPXMock):
    with open(Path(__file__).parent / "data" / "test_search_data.json", "r") as f:
        test_json_search_response = json.loads(f.read())
    httpx_mock.add_response(json=test_json_search_response)

    search_results: SearchContent = await search_odata(
        long=0.0,
        lat=0.0,
        cloud_coverage=25.0,
        time_lt="",
        time_gt="",
        max_=10,
    )
    assert len(search_results.value) == 10
