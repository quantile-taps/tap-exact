"""Exact Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from singer_sdk.helpers._util import utc_now
from singer_sdk.streams import RESTStream
import backoff
import requests
import json
import boto3


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
        self.s3 = boto3.client("s3")
        tokens = self.download_tokens_from_s3()
        self._auth_endpoint = "https://start.exactonline.nl/api/oauth2/token"
        self._default_expiration = 600
        self.refresh_token = tokens["refresh_token"]
        self.access_token = tokens["access_token"]

    def download_tokens_from_s3(self) -> dict:
        return json.loads(
            self.s3.get_object(
                Bucket=self._config["tokens_s3_bucket"], Key=self._config["tokens_s3_key"] + "/tokens.json"
            )
            .get("Body")
            .read()
        )

    def put_tokens_in_s3(self, tokens: dict) -> None:
        self.s3.put_object(
            Bucket=self._config["tokens_s3_bucket"],
            Key=self._config["tokens_s3_key"] + "/tokens.json",
            Body=json.dumps(tokens, indent=4),
        )

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the AutomaticTestTap API.

        Returns:
            A dict with the request body
        """
        return {
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
        }

    @backoff.on_exception(backoff.expo, EmptyResponseError, max_tries=5, factor=2)
    def update_access_token(self) -> None:
        request_time = utc_now()
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(
            self.auth_endpoint,
            headers=self._oauth_headers,
            data=auth_request_payload,
            timeout=60,
        )

        try:
            if token_response.json().get("error_description") == "Rate limit exceeded: access_token not expired":
                return None
        except Exception as e:
            raise EmptyResponseError(f"Failed converting response to a json, because response is empty")

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

        tokens = {"access_token": self.access_token, "refresh_token": self.refresh_token}
        self.put_tokens_in_s3(tokens)
