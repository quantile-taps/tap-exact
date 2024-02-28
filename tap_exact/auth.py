"""Exact Authentication."""
from __future__ import annotations

import backoff
import os
import json
import requests
import pendulum

from smart_open import open
from functools import cached_property

from singer_sdk.helpers._util import utc_now
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


class EmptyResponseError(Exception):
    """Raised when the response is empty"""


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class ExactAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Exact."""

    def __init__(self, stream: RESTStream) -> None:
        """Init authenticator.

        Args:
            stream: A stream for a RESTful endpoint.
        """
        super().__init__(stream)
        self._auth_endpoint = "https://start.exactonline.nl/api/oauth2/token"
        self._default_expiration = 600
        
        tokens = self.load_tokens_from_blob()

        self.access_token = tokens["access_token"]
        self.refresh_token = tokens["refresh_token"]
        self.last_refreshed = pendulum.parse(tokens["last_refreshed"])
        self.expires_in = 600
        
    @cached_property
    def azure_client(self):
        from azure.storage.blob import BlobServiceClient

        return BlobServiceClient.from_connection_string(
            self.config["azure_connection_string"]
        )
    
    def load_tokens_from_blob(self) -> dict:
        """Loads Exact Online tokens from Azure blob storage using smart_open.

        Returns:
            A dict with the tokens.
        """
        with open(self.config["blob_storage_path"], "r", transport_params={"client": self.azure_client}) as token_file:
            tokens = json.load(token_file)

        return tokens
    
    def update_tokens_in_blob(self, tokens: dict) -> None:
        """Updates Exact Online tokens in Azure blob storage using smart_open.

        Args:
            tokens: A dict with the tokens.
        """
        with open(self.config["blob_storage_path"], "w", transport_params={"client": self.azure_client}) as token_file:
            json.dump(tokens, token_file)

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Exact Online API.

        Returns:
            A dict with the request body
        """
        return {
            "refresh_token": self.refresh_token,
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "grant_type": "refresh_token",
        }

    @backoff.on_exception(backoff.expo, EmptyResponseError, max_tries=5, factor=2)
    def update_access_token(self) -> None:
        """Update the access token."""

        # Get the current time to calculate the token expiration
        request_time = utc_now()

        # Set the OAuth request payload
        auth_request_payload = self.oauth_request_payload

        # Make the OAuth request to the authentication endpoint
        token_response = requests.post(
            self.auth_endpoint,
            headers=self._oauth_headers,
            data=auth_request_payload,
            timeout=60,
        )

        # Raise an error if the request was not successful
        try:
            token_response.raise_for_status()
        except requests.HTTPError as ex:
            msg = f"Failed OAuth login, response was '{token_response.json()}'. {ex}"
            raise RuntimeError(msg) from ex

        self.logger.info("OAuth authorization attempt was successful.")

        token_json = token_response.json()

        self.access_token = token_json["access_token"]
        self.refresh_token = token_json["refresh_token"]

        expiration = token_json.get("expires_in", self._default_expiration)

        self.expires_in = int(expiration) if expiration else None

        if self.expires_in is None:
            self.logger.debug(
                "No expires_in receied in OAuth response and no "
                "default_expiration set. Token will be treated as if it never "
                "expires.",
            )

        self.last_refreshed = request_time

        # Update the tokens in Azure blob storage
        tokens = {
            "access_token": self.access_token, 
            "refresh_token": self.refresh_token,
            "last_refreshed": self.last_refreshed.to_iso8601_string()
        }
        
        self.update_tokens_in_blob(tokens)
