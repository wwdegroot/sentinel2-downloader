import msgspec
from dotenv import load_dotenv
import asyncio
from rich import print
import asyncclick as click
from rich.prompt import Prompt
from st2dl.auth import get_access_token
from st2dl.download.preview import get_preview_download_links
from st2dl.download.product import download_products_data
from st2dl.cli import wkt_to_point, show_preview_urls, daterange_to_timestamp
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
    type=click.BOOL,
    show_default=True,
    help="Debug the http requests and extra debug logging",
)
async def main(
    pointofinterest: str,
    daterange: str,
    max_: int,
    cloud_coverage: float,
    username: str,
    password: str,
    debug: bool,
):
    """
    POINTOFINTEREST the point WKT string which is used for the intersect with sentinel 2 data. SRID=4326. Example: "POINT(-9.1372 38.7000)"

    DATERANGE the range of dates comma seperated between which is searched. For example: "11-08-2023 00:00:00,11-09-2023 00:00:00"
    \f
    :param pointofinterest:
    :param max_:
    :param cloud_coverage:
    :param username:
    :param password:
    :param debug:
    :return:
    """

    long, lat = wkt_to_point(pointofinterest)
    time_gt, time_lt = daterange_to_timestamp(daterange)
    print(f"coordinates: lat: {lat:.4f}, long: {long:.4f}")
    print(f"maximum results: {max_}")
    print(f"cloud coverage percentage less then: {cloud_coverage:.2f}")

    search_data = await search_odata(long, lat, cloud_coverage, time_lt, time_gt, max_)
    if debug:
        with open("../search_data.json", "wb") as f:
            f.write(msgspec.json.encode(search_data))
    preview_urls = get_preview_download_links(search_data)
    show_preview_urls(preview_urls)
    prompt = Prompt()
    preview_download = prompt.ask(
        "Which preview images id's need to be downloaded, seperate multiple choices by ,",
        # choices=[str(item['id']) for item in preview_urls],
    )
    download_product_ids = [
        item["productid"]
        for item in preview_urls
        if item["id"] in [n for n in preview_download.split(",")]
    ]
    tokens = get_access_token(username, password)

    download_products_data(download_product_ids, tokens.access_token)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
