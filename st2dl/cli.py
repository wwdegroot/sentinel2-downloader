from typing import Tuple, List

from rich.table import Table
from rich.console import Console
import re
from datetime import datetime
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from st2dl.exceptions import InvalidWktPointArgument


progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)


# "2022-05-03T00:00:00.000Z"
ESA_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def convert_to_timestamp(datestring="", dateformat="%d-%m-%Y %H:%M:%S"):
    if len(datestring) > 10:
        source = datetime.strptime(datestring, dateformat)
    else:
        source = datetime.strptime(datestring, "%d-%m-%Y")
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
    table.add_column("ID", justify="left", style="magenta")
    table.add_column("Preview", justify="left", style="blue")
    table.add_column("Name", justify="left", style="magenta")

    for entry in preview_urls:
        table.add_row(
            entry["id"],
            f'[link={entry["url"].replace("(", "%28").replace(")", "%29")}]{entry["origindate"]}[/link]',
            entry["name"],
        )

    console = Console()
    console.print(table)
