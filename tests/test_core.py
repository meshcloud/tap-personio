"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_personio.tap import Tappersonio

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
    "client_id": "abc",
    "client_secret": "xyz"
}


# Run standard built-in tap tests from the SDK:
TestTappersonio = get_tap_test_class(
    tap_class=Tappersonio,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
