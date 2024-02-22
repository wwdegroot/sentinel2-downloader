from typing import List
import signal
import httpx
from rich.progress import TaskID, Event
from st2dl.cli import progress
from st2dl.download.search import SearchResult

done_event = Event()


# do it with a live progress: https://github.com/Textualize/rich/blob/master/examples/live_progress.py
def handle_sigint(signum, frame):
    done_event.set()


signal.signal(signal.SIGINT, handle_sigint)


async def download_tci_products_data(
    task_id: TaskID, product: SearchResult, access_token: str, mm_band: str = "R10m"
):
    headers = {"Authorization": f"Bearer {access_token}"}
    progress.start_task(task_id)
    async with httpx.AsyncClient() as client:
        client.headers.update(headers)
        # create the tci image url
        granule_url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product.id})/Nodes({product.name})/Nodes(GRANULE)/Nodes"
        granule_resp = await client.get(
            f"{granule_url}", follow_redirects=True, headers=headers
        )
        granule_folder = granule_resp.json()
        img_data_url = f"{granule_url}({granule_folder['result'][0]['Name']})/Nodes(IMG_DATA)/Nodes({mm_band})/Nodes"
        img_data_resp = await client.get(img_data_url, follow_redirects=True)
        img_data = img_data_resp.json()
        tci_name = [img["Name"] for img in img_data["result"] if "TCI" in img["Name"]][
            0
        ]
        tci_url = f"{img_data_url}({tci_name})/$value"
        async with client.stream(
            method="GET",
            url=tci_url,
            headers=headers,
        ) as response:
            progress.update(task_id, total=int(response.headers["Content-length"]))
            with open(f"{tci_name}", "wb") as file:
                progress.start_task(task_id)
                async for chunk in response.aiter_bytes():
                    if chunk:
                        file.write(chunk)
                        progress.update(task_id, advance=len(chunk))
                        if done_event.is_set():
                            return
        progress.console.log(f"Downloaded {tci_name}")


async def download_data(task_id: TaskID, product: SearchResult, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        client.headers.update(headers)
        async with client.stream(
            "GET",
            url=f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product.id})/$value",
            headers=headers,
        ) as response:
            progress.update(task_id, total=int(response.headers["Content-length"]))
            with open(f"product-{product.id}.zip", "wb") as file:
                progress.start_task(task_id)
                async for chunk in response.aiter_bytes():
                    if chunk:
                        file.write(chunk)
                        progress.update(task_id, advance=len(chunk))
                        if done_event.is_set():
                            return
    progress.console.log(f"Downloaded product-{product.id}.zip")


async def download_products_data(
    products: List[SearchResult], access_token: str, tci_only: bool = False
):
    with progress:
        for product in products:
            task_id = progress.add_task(
                f"product-{product.id}",
                filename=f"product-{product.id}.zip",
                start=False,
            )
            if tci_only:
                await download_tci_products_data(task_id, product, access_token)
            else:
                await download_data(task_id, product, access_token)
