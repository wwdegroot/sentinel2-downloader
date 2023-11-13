from typing import Tuple, List

from rich.table import Table
from rich.console import Console
import re
from datetime import datetime
from st2dl.exceptions import InvalidWktPointArgument


# "2022-05-03T00:00:00.000Z"
ESA_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def convert_to_timestamp(datestring="", dateformat="%d-%m-%Y %H:%M:%S"):
    source = datetime.strptime(datestring, dateformat)
    return source.strftime(ESA_DATE_FORMAT)


def wkt_to_point(wktstring: str) -> Tuple[float, ...]:
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", wktstring)
    if len(nums) != 2:
        raise InvalidWktPointArgument(
            f"Give a valid WKT string. for example: POINT(-9.1372 38.7000). WKT received: {wktstring}"
        )
    return tuple(float(n) for n in nums)


def show_preview_urls(preview_urls: List[dict[str, str]]) -> None:
    table = Table(title="Sentinel-2 Preview Url's")
    table.add_column("OriginDate", justify="left", style="cyan")
    table.add_column("Url", justify="left", style="blue")
    table.add_column("Name", justify="left", style="magenta")

    for entry in preview_urls:
        table.add_row(
            entry["origindate"],
            entry["url"].replace("(", "%28").replace(")", "%29"),
            entry["name"],
        )

    console = Console()
    console.print(table)
