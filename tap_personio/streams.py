"""Stream type classes for tap-personio."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_personio.client import PersonioStream

class EmployeesStream(PersonioStream):
    """Define custom stream."""

    name = "employess"
    path = "/company/employees"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    schema = th.PropertiesList(
        th.Property(
            "id",
            th.StringType,
            description="The user's system ID",
        ),
        th.Property("name", th.StringType),
        th.Property(
            "email",
            th.StringType,
            description="The user's email address",
        )
    ).to_dict()

    records_jsonpath = "$.data[*]"

