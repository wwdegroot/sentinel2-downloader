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


def download_data(task_id: TaskID, product_id: str, access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    with httpx.Client() as client:
        client.headers.update(headers)
        with client.stream(
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
