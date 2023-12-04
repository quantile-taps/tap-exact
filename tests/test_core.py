"""Tests standard tap features using the built-in SDK tests library."""

from datetime import datetime, timedelta
import os

from singer_sdk.testing import get_tap_test_class

from tap_exact.tap import TapExact

SAMPLE_CONFIG = {
    "start_date": (datetime.now(datetime.timezone.utc) - timedelta(days=50)).strftime("%Y-%m-%d"),
    "client_id": os.getenv("TAP_EXACT_CLIENT_ID"),
    "client_secret": os.getenv("TAP_EXACT_CLIENT_SECRET"),
    "tokens_s3_bucket": "ticketswap-redshift-reporting",
    "tokens_s3_key": "datajobs/exactonline",
    "division": "3490573",
}


# Run standard built-in tap tests from the SDK:
TestTapExact = get_tap_test_class(
    tap_class=TapExact,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
