"""Personio Authentication."""

from __future__ import annotations
import requests

from singer_sdk.helpers._util import utc_now
from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta

# Personio API tokens beahve like OTPs:
# "The bearer token can then used to access any Personnel Data endpoint (i.e. all endpoints except Auth and Recruiting)
#  but please note that the bearer token can be used for only one request and is blacklisted immediately after its use.
# https://developer.personio.de/reference/auth
class PersonioAuthenticator(OAuthAuthenticator):
    """Authenticator class for personio."""

    @property
    def oauth_request_body(self) -> dict:
        
        """Define the OAuth request body for the Personio API.

        Returns:
            A dict with the request body
        """
        return {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"]
        }

    # Override base class implementation to deal with personio's non-standard auth endpoint  https://developer.personio.de/reference/post_auth
    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        self.logger.warning("UPDATING ACCES TOKEN")

        request_time = utc_now()
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(
            self.auth_endpoint,
            data=auth_request_payload,
            timeout=60,
        )
        try:
            token_response.raise_for_status()
        except requests.HTTPError as ex:
            msg = f"Failed OAuth login, response was '{token_response.json()}'. {ex}"
            raise RuntimeError(msg) from ex

        self.logger.info("OAuth authorization attempt was successful.")

        token_json = token_response.json()
        self.access_token = token_json["data"]["token"]
        self.expires_in = 0; # immediately expire the token        
        self.last_refreshed = request_time

    

    @classmethod
    def create_for_stream(cls, stream) -> PersonioAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint="https://api.personio.de/v1/auth",
            oauth_scopes="",
        )
