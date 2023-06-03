"""Stream type classes for tap-personio."""

from __future__ import annotations

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_personio.client import PersonioStream

class EmployeesDiscoveryStream(PersonioStream):
    """Define custom stream."""

    name = "employees"
    path = "/company/employees"
    primary_keys = ["id"]
    replication_key = None

    records_jsonpath = "$.data[*].attributes"

    @property
    def schema(self):
        return th.PropertiesList().to_dict()

class EmployeesStream(EmployeesDiscoveryStream):
    discovered_schema = None

    @property
    def schema(self):
        """Dynamically detect the json schema for the stream.
        This is evaluated prior to any records being retrieved.
        """

        if self.discovered_schema != None:
            return self.discovered_schema
   
        properties: List[th.Property] = []
        
        # id is mandatory and always present, the rest depends on the configuration of the API token
        properties.append(
            th.Property(
                "id",
                th.IntegerType,
                description="The user's system ID",
            )
        )

        # hack: we have to discover the schema dynmically based on the data that's coming off personio
        # however, we can't just make an http request from this class instance since .schema is called from the 
        # ctor (bad! never call a virtual function from a ctor...) and thus all the http stuff is not initialized yet.
        # We therefore create a separate instance of our base class that has a purposefully empty schema to make that 
        # request, then build our schema off of that.
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

    