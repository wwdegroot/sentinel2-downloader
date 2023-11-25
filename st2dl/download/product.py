from concurrent.futures import ThreadPoolExecutor
from typing import List
import signal
import httpx
from rich.progress import TaskID, Event
from st2dl.cli import progress


done_event = Event()


def handle_sigint(signum, frame):
    done_event.set()


signal.signal(signal.SIGINT, handle_sigint)


# TODO: download the TCI directly.
#  url template:
#  https://zipper.dataspace.copernicus.eu/odata/v1/Products(223e039f-990c-42fb-8824-a0264edac49f)/Nodes(S2A_MSIL2A_20230812T112121_N0509_R037_T29SMC_20230812T173903.SAFE)/Nodes(GRANULE)/Nodes(L2A_T29SMC_A042505_20230812T112234)/Nodes(IMG_DATA)/Nodes(R10m)/Nodes(T29SMC_20230812T112121_TCI_10m.jp2)/$value
#  Guess each node needs to be traversed to get to the 10m tci image
async def download_tci_data(
    task_id: TaskID, product_id: str, mm_band: str, access_token: str
):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        client.headers.update(headers)


async def download_data(task_id: TaskID, product_id: str, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient() as client:
        client.headers.update(headers)
        async with client.stream(
            "GET",
            url=f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value",
            headers=headers,
        ) as response:
            progress.update(task_id, total=int(response.headers["Content-length"]))
            with open(f"product-{product_id}.zip", "wb") as file:
                progress.start_task(task_id)
                for chunk in response.iter_bytes():
                    if chunk:
                        file.write(chunk)
                        progress.update(task_id, advance=len(chunk))
                        if done_event.is_set():
                            return
    progress.console.log(f"Downloaded product-{product_id}.zip")


def download_products_data(product_ids: List[str], access_token: str):
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for product_id in product_ids:
                task_id = progress.add_task(
                    f"product-{product_id}",
                    filename=f"product-{product_id}.zip",
                    start=False,
                )
                pool.submit(download_data, task_id, product_id, access_token)
