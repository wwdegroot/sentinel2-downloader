from typing import List


def get_preview_download_links(search_json) -> List[str]:
    return [v["Assets"][0]["DownloadLink"] for v in search_json["value"]]
