"""REST client handling, including ExactStream base class."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Iterable, Optional, Dict
import typing
from datetime import datetime

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseOffsetPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
from lxml import etree
import json
import xmltodict
from pendulum import parse

from tap_exact.auth import ExactAuthenticator

if typing.TYPE_CHECKING:
    from requests import Response

TPageToken = typing.TypeVar("TPageToken")

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ExactPaginator(BaseOffsetPaginator):
    def __init__(self, stream, start_value, page_size) -> None:
        super().__init__(start_value=start_value, page_size=page_size)
        self.stream = stream

    def has_more(self, response: Response) -> bool:  # noqa: ARG002
        """Override this method to check if the endpoint has any pages left.

        Args:
            response: API response object.

        Returns:
            Boolean flag used to indicate if the endpoint has more pages.
        """
        data = self.stream.xml_to_dict(response)
        link = data.get("feed", {}).get("link", [])
        if type(link) == list:
            return "next" in [item.get("@rel", "") for item in link]

    def get_next(self, response: Response) -> TPageToken | None:
        """Get the next pagination token or index from the API response.

        Args:
            response: API response object.

        Returns:
            The next page token or index. Return `None` from this method to indicate
                the end of pagination.
        """
        data = self.stream.xml_to_dict(response)
        link = data.get("feed", {}).get("link", [])
        if "next" in [item.get("@rel", "") for item in link]:
            next_link = [item["@href"] for item in link if item["@rel"] == "next"][0]
            next_page_token = next_link.split("&")[-1].split("=")[-1]
            return next_page_token


class ExactStream(RESTStream):
    """Exact stream class."""

    @property
    def partitions(self) -> list[dict] | None:
        return [{"division": division} for division in self.config["divisions"]]

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return f"https://start.exactonline.nl/api/v1"

    def get_url(self, context: dict | None) -> str:
        return f"{self.url_base}/{context['division']}{self.path}"

    @cached_property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return ExactAuthenticator(self)

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        replication_key = self.get_starting_timestamp(context)
        return replication_key or start_date

    def get_url_params(self, context: Optional[dict], next_page_token) -> Dict[str, Any]:
        params: dict = {}
        if self.select:
            params["$select"] = self.select
        start_date = self.get_starting_time(context).strftime("%Y-%m-%dT%H:%M:%S")
        if self.replication_key:
            date_filter = f"Modified gt datetime'{start_date}'"
            params["$filter"] = date_filter
        if next_page_token:
            params["$skiptoken"] = next_page_token
        return params

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Create a new pagination helper instance."""
        return ExactPaginator(self, start_value=None, page_size=60)

    def xml_to_dict(self, response):
        try:
            # clean invalid xml characters
            my_parser = etree.XMLParser(recover=True)
            xml = etree.fromstring(response.content, parser=my_parser)
            cleaned_xml_string = etree.tostring(xml)
            # parse xml to dict
            data = json.loads(json.dumps(xmltodict.parse(cleaned_xml_string)))
        except:
            data = json.loads(json.dumps(xmltodict.parse(response.content.decode("utf-8-sig").encode("utf-8"))))
        return data

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        data = self.xml_to_dict(response).get("feed", {}).get("entry", [])
        yield from extract_jsonpath(self.records_jsonpath, input=data)

    def post_process(
        self,
        row: dict,
        context: dict | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        content = row["content"]["m:properties"]
        new_content = {}
        for key, value in content.items():
            new_key = key[2:]
            if type(value) == str:
                new_content[new_key] = value
            elif not value or value.get("@m:null") == "true":
                new_content[new_key] = None
            elif value.get("@m:type") == "Edm.Boolean":
                if value.get("#text") == "true":
                    new_content[new_key] = True
                elif value.get("#text") == "false":
                    new_content[new_key] = False
                else:
                    new_content[new_key] = None
            elif "Int" in value.get("@m:type", ""):
                new_content[new_key] = int(value.get("#text"))
            elif "Double" in value.get("@m:type", ""):
                new_content[new_key] = float(value.get("#text"))
            else:
                new_content[new_key] = value.get("#text", None)
        row = new_content
        return row

    @property
    def select(self):
        return ",".join(self.schema["properties"].keys())


class ExactSyncStream(ExactStream):
    """Exact sync stream class."""

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Create a new pagination helper instance."""
        return ExactPaginator(self, start_value=None, page_size=1000)

    def get_starting_time(self, context):
        state = self.get_context_state(context)
        rep_key = None
        if "replication_key_value" in state.keys():
            rep_key = state["replication_key_value"]
        return rep_key or 1

    def get_url_params(self, context: Optional[dict], next_page_token) -> Dict[str, Any]:
        params: dict = {}
        if self.select:
            params["$select"] = self.select
        start_timestamp = self.get_starting_time(context)
        if start_timestamp == 1:
            date_filter = f"Timestamp gt {start_timestamp}"
        else:
            date_filter = f"Timestamp gt {start_timestamp}L"
        params["$filter"] = date_filter
        if next_page_token:
            params["$skiptoken"] = next_page_token
        return params
