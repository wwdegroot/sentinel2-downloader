import sys
from datetime import datetime
from dotenv import load_dotenv
import httpx
import orjson
from rich import print
from core.preview import get_preview_download_links


# "2022-05-03T00:00:00.000Z"
ESA_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def convert_to_timestamp(datestring="", dateformat="%d-%m-%Y %H:%M:%S"):
    source = datetime.strptime(datestring, dateformat)
    return source.strftime(ESA_DATE_FORMAT)


def main():
    # username = os.getenv("ESA_USERNAME")
    # userpass = os.getenv("ESA_USERPASS")
    esa_search_url = r"https://catalogue.dataspace.copernicus.eu/odata/v1/Products"

    # long lat
    geom = "-9.1372 38.7000"

    time_gt = convert_to_timestamp(datestring="11-08-2023 00:00:00")
    time_lt = convert_to_timestamp(datestring="11-09-2023 00:00:00")

    cloud_cover_percentage: float = 25.00
    max_results = 10
    # filter voor zoeken op cloudCover, Productype en orbitDirection.
    # lt = less then
    # eq = equal to
    # gt = greater then
    search_filter = f"OData.CSC.Intersects(area=geography'SRID=4326;POINT ({geom})') and Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value lt {cloud_cover_percentage:.2f}) and Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI2A') and ContentDate/Start gt {time_gt} and ContentDate/Start lt {time_lt}"
    with httpx.Client() as client:
        # client.auth = (username, userpass)
        r = client.get(
            url=f"{esa_search_url}?$filter={search_filter}&$top={max_results}&$expand=Assets",
            timeout=60,
        )
        if not r.status_code == 200:
            print(f"Error getting data: {r.text}")
            sys.exit(-1)
        search_data = r.json()
        with open("search_data.json", "wb") as f:
            f.write(orjson.dumps(search_data))

    preview_urls = get_preview_download_links(search_data)
    print(preview_urls)


if __name__ == "__main__":
    load_dotenv()
    main()
