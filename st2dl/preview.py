from typing import List


def get_preview_download_links(search_json) -> List[dict[str, str]]:
    return [
        {
            "url": v["Assets"][0]["DownloadLink"],
            "origindate": v["OriginDate"],
            "name": v["Name"],
        }
        for v in search_json["value"]
    ]
