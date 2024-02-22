from typing import List

import msgspec
from dotenv import load_dotenv
import asyncio
from rich import print
import asyncclick as click
from rich.prompt import Prompt
from st2dl.auth import get_access_token
from st2dl.download.product import download_products_data
from st2dl.cli import (
    wkt_to_point,
    show_preview_urls,
    daterange_to_timestamp,
    Preview,
    get_selected_products,
)
from st2dl.download.search import search_odata


@click.command()
@click.argument("pointofinterest", type=click.STRING)
@click.argument("daterange", type=click.STRING)
@click.option(
    "--username",
    "-u",
    type=click.STRING,
    help="Username for Copernicus Data Space Ecosystem",
)
@click.option(
    "--password", "-p", prompt=True, hide_input=True, confirmation_prompt=False
)
@click.option(
    "--max",
    "-m",
    "max_",
    default=20,
    type=click.INT,
    show_default=True,
    help="maximum number of results returned",
)
@click.option(
    "--cloud-coverage",
    "-c",
    "cloud_coverage",
    default=25.00,
    type=click.FLOAT,
    show_default=True,
    help="Get only results with a cloud coverage percentage less then the argument given.",
)
@click.option(
    "--debug",
    default=False,
    is_flag=True,
    type=click.BOOL,
    show_default=True,
    help="Debug the http requests and extra debug logging",
)
@click.option(
    "--tci",
    default=False,
    is_flag=True,
    type=click.BOOL,
    show_default=True,
    help="Download only True Color Image (TCI)",
)
async def main(
    pointofinterest: str,
    daterange: str,
    max_: int,
    cloud_coverage: float,
    username: str,
    password: str,
    debug: bool,
    tci: bool,
):
    """
    POINTOFINTEREST the point WKT string which is used for the intersect with sentinel 2 data. SRID=4326. Example: "POINT(-9.1372 38.7000)"

    DATERANGE the range of dates comma seperated between which is searched. For example: "11-08-2023 00:00:00,11-09-2023 00:00:00"
    \f
    :param pointofinterest:
    :param daterange:
    :param max_:
    :param cloud_coverage:
    :param username:
    :param password:
    :param debug:
    :param tci:
    :return:
    """

    long, lat = wkt_to_point(pointofinterest)
    time_gt, time_lt = daterange_to_timestamp(daterange)
    print(f"coordinates: lat: {lat:.4f}, long: {long:.4f}")
    print(f"maximum results: {max_}")
    print(f"cloud coverage percentage less then: {cloud_coverage:.2f}")

    search_data = await search_odata(long, lat, cloud_coverage, time_lt, time_gt, max_)
    if debug:
        print("DEBUG: Search request data is saved to disk.")
        with open("search_data.json", "wb") as f:
            f.write(msgspec.json.encode(search_data))
    preview_urls: List[Preview] = show_preview_urls(search_data)
    prompt = Prompt()
    preview_download = prompt.ask(
        "Which preview images id's need to be downloaded, separate multiple choices by a comma ','",
        # choices=[str(item['id']) for item in preview_urls],
    )
    products_to_download = get_selected_products(
        search_json=search_data, preview_urls=preview_urls, product_ids=preview_download
    )
    tokens = get_access_token(username, password)

    await download_products_data(
        products_to_download, tokens.access_token, tci_only=tci
    )


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
