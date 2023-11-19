from typing import List
import msgspec


class Preview(msgspec.Struct):
    id: str
    productid: str
    url: str
    origindate: str
    name: str


def get_preview_download_links(search_json) -> List[dict[str, str]]:
    return [
        {
            "id": str(i),
            "productid": v["Id"],
            "url": v["Assets"][0]["DownloadLink"],
            "origindate": v["OriginDate"],
            "name": v["Name"],
        }
        for i, v in enumerate(search_json["value"])
    ]
