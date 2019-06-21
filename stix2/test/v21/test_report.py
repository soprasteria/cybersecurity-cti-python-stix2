import datetime as dt

import pytest
import pytz

import stix2

from .constants import INDICATOR_KWARGS, REPORT_ID

EXPECTED = """{
    "type": "report",
    "spec_version": "2.1",
    "id": "report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
    "created_by_ref": "identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283",
    "created": "2015-12-21T19:59:11.000Z",
    "modified": "2015-12-21T19:59:11.000Z",
    "name": "The Black Vine Cyberespionage Group",
    "description": "A simple report with an indicator and campaign",
    "report_types": [
        "campaign"
    ],
    "published": "2016-01-20T17:00:00Z",
    "object_refs": [
        "indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2",
        "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
        "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a"
    ]
}"""


def test_report_example():
    report = stix2.v21.Report(
        id="report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
        created_by_ref="identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283",
        created="2015-12-21T19:59:11.000Z",
        modified="2015-12-21T19:59:11.000Z",
        name="The Black Vine Cyberespionage Group",
        description="A simple report with an indicator and campaign",
        published="2016-01-20T17:00:00Z",
        report_types=["campaign"],
        object_refs=[
            "indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2",
            "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
            "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a",
        ],
    )

    assert str(report) == EXPECTED


def test_report_example_objects_in_object_refs():
    report = stix2.v21.Report(
        id="report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
        created_by_ref="identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283",
        created="2015-12-21T19:59:11.000Z",
        modified="2015-12-21T19:59:11.000Z",
        name="The Black Vine Cyberespionage Group",
        description="A simple report with an indicator and campaign",
        published="2016-01-20T17:00:00Z",
        report_types=["campaign"],
        object_refs=[
            stix2.v21.Indicator(id="indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2", **INDICATOR_KWARGS),
            "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
            "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a",
        ],
    )

    assert str(report) == EXPECTED


def test_report_example_objects_in_object_refs_with_bad_id():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v21.Report(
            id="report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
            created_by_ref="identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283",
            created="2015-12-21T19:59:11.000Z",
            modified="2015-12-21T19:59:11.000Z",
            name="The Black Vine Cyberespionage Group",
            description="A simple report with an indicator and campaign",
            published="2016-01-20T17:00:00Z",
            report_types=["campaign"],
            object_refs=[
                stix2.v21.Indicator(id="indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2", **INDICATOR_KWARGS),
                "campaign-83422c77-904c-4dc1-aff5-5c38f3a2c55c",   # the "bad" id, missing a "-"
                "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a",
            ],
        )

    assert excinfo.value.cls == stix2.v21.Report
    assert excinfo.value.prop_name == "object_refs"


@pytest.mark.parametrize(
    "data", [
        EXPECTED,
        {
            "created": "2015-12-21T19:59:11.000Z",
            "created_by_ref": "identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283",
            "description": "A simple report with an indicator and campaign",
            "id": "report--84e4d88f-44ea-4bcd-bbf3-b2c1c320bcb3",
            "report_types": [
                "campaign",
            ],
            "modified": "2015-12-21T19:59:11.000Z",
            "name": "The Black Vine Cyberespionage Group",
            "object_refs": [
                "indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2",
                "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
                "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a",
            ],
            "published": "2016-01-20T17:00:00Z",
            "spec_version": "2.1",
            "type": "report",
        },
    ],
)
def test_parse_report(data):
    rept = stix2.parse(data, version="2.1")

    assert rept.type == 'report'
    assert rept.spec_version == '2.1'
    assert rept.id == REPORT_ID
    assert rept.created == dt.datetime(2015, 12, 21, 19, 59, 11, tzinfo=pytz.utc)
    assert rept.modified == dt.datetime(2015, 12, 21, 19, 59, 11, tzinfo=pytz.utc)
    assert rept.created_by_ref == "identity--a463ffb3-1bd9-4d94-b02d-74e4f1658283"
    assert rept.object_refs == [
        "indicator--26ffb872-1dd9-446e-b6f5-d58527e5b5d2",
        "campaign--83422c77-904c-4dc1-aff5-5c38f3a2c55c",
        "relationship--f82356ae-fe6c-437c-9c24-6b64314ae68a",
    ]
    assert rept.description == "A simple report with an indicator and campaign"
    assert rept.report_types == ["campaign"]
    assert rept.name == "The Black Vine Cyberespionage Group"

# TODO: Add other examples
