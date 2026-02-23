"""dlt pipeline to ingest NYC taxi data from the Zoomcamp REST API."""

import dlt
import os
from pathlib import Path
from dlt.sources.rest_api import rest_api_source
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def nyc_taxi_rest_api_source() -> dlt.sources.DltSource:
    """Define dlt resources for the NYC taxi REST API."""
    # Optional helper for faster local runs:
    # set `TAXI_MAX_PAGE=5` to limit pages ingested.
    max_page_env = os.getenv("TAXI_MAX_PAGE")
    max_page = int(max_page_env) if max_page_env and max_page_env.isdigit() else None

    paginator: dict = {
        "type": "page_number",
        # API returns 1,000 records per page and stops on empty page.
        "base_page": 1,
        "page_param": "page",
        # API does not return a "total" field; rely on empty page to stop.
        "total_path": None,
        "stop_after_empty_page": True,
    }
    if max_page is not None:
        paginator["maximum_page"] = max_page

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        },
        "resources": [
            {
                "name": "nyc_taxi_trips",
                "endpoint": {
                    # Base URL already points to the function; no extra path segment.
                    "path": "",
                    "method": "GET",
                    "paginator": paginator,
                },
            }
        ],
    }

    return rest_api_source(config)


taxi_pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    # Keep pipeline working files out of OneDrive-synced folders (avoids WinError 5 locks)
    pipelines_dir=str(Path.home() / ".dlt" / "pipelines"),
    # Store data in a local DuckDB file in this project folder
    destination=dlt.destinations.duckdb(str(Path(__file__).resolve().parent / "taxi_pipeline.duckdb")),
    dataset_name="nyc_taxi_data",
    dev_mode=True,
    progress="log",
)


if __name__ == "__main__":
    load_info = taxi_pipeline.run(nyc_taxi_rest_api_source())
    print(load_info)  # noqa: T201

