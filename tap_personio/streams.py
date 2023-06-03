"""Stream type classes for tap-personio."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_personio.client import PersonioStream

class EmployeesDiscoveryStream(PersonioStream):
    """Define custom stream."""

    name = "employees"
    path = "/company/employees"
    primary_keys = ["id"]

    @property
    def schema(self):
        return th.PropertiesList().to_dict()

class EmployeesStream(PersonioStream):
    """Define custom stream."""

    name = "employees"
    path = "/company/employees"
    primary_keys = ["id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    
    # schema_filepath = SCHEMAS_DIR / "users.json"  # noqa: ERA001
    
    discovered_schema = None

    @property
    def schema(self):
        """Dynamically detect the json schema for the stream.
        This is evaluated prior to any records being retrieved.
        """

        if self.discovered_schema != None:
            return self.discovered_schema

        self.logger.info("DISCOVERING SCHEMA")
        
        properties: List[th.Property] = []
        
        # id is mandatory and always present, the rest depends on the configuration of the API token
        properties.append(
            th.Property(
                "id",
                th.IntegerType,
                description="The user's system ID",
            )
        )


        hack = EmployeesDiscoveryStream(self._tap, "discover_employees", {}, None)

        for records in hack.request_records(None):
            first_record = records["data"][0]

            if first_record:
                for attr in first_record["attributes"]:
                    properties.append(th.Property(attr, th.StringType()))            

            # we always abort the iterator after fetching the first record
            break
            
        self.discovered_schema = th.PropertiesList(*properties).to_dict()
        return self.discovered_schema
    
    records_jsonpath = "$.data[*].attributes"

    