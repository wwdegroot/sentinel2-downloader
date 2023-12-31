import sys
from dotenv import load_dotenv
import httpx
import orjson
from rich import print
import click
from rich.prompt import Prompt
from st2dl.auth import get_access_token
from st2dl.preview import get_preview_download_links
from st2dl.product import download_products_data
from st2dl.cli import convert_to_timestamp, wkt_to_point, show_preview_urls


@click.command()
@click.argument("pointofinterest", type=click.STRING)
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
def main(
    pointofinterest: str,
    max_: int,
    cloud_coverage: float,
    username: str,
    password: str,
    debug: bool,
):
    """
    POINTOFINTEREST the point WKT string which is used for the intersect with sentinel 2 data. SRID=4326. Example: "POINT(-9.1372 38.7000)"

    \f
    :param pointofinterest:
    :param max_:
    :param cloud_coverage:
    :return:
    """
    esa_search_url = r"https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    long, lat = wkt_to_point(pointofinterest)
    print(f"coordinates: lat: {lat:.4f}, long: {long:.4f}")
    print(f"maximum results: {max_}")
    print(f"cloud coverage percentage less then: {cloud_coverage:.2f}")
    time_gt = convert_to_timestamp(datestring="11-08-2023 00:00:00")
    time_lt = convert_to_timestamp(datestring="11-09-2023 00:00:00")
    # filter voor zoeken op cloudCover, Productype en orbitDirection.
    # lt = less then
    # eq = equal to
    # gt = greater then
    search_filter = f"OData.CSC.Intersects(area=geography'SRID=4326;POINT ({long:.4f} {lat:.4f})') and Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value lt {cloud_coverage:.2f}) and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI2A') and ContentDate/Start gt {time_gt} and ContentDate/Start lt {time_lt}"
    with httpx.Client() as client:
        r = client.get(
            url=f"{esa_search_url}?$filter={search_filter}&$top={max_}&$expand=Assets",
            timeout=60,
        )
        if not r.status_code == 200:
            print(f"Error getting data: {r.text}")
            sys.exit(-1)
        search_data = r.json()
        if debug:
            with open("../search_data.json", "wb") as f:
                f.write(orjson.dumps(search_data))

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
    main()
