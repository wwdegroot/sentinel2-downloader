from typing import List


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
