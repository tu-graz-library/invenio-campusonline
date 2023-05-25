# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module utils."""

from xml.etree.ElementTree import Element

from invenio_campusonline.types import Embargo
from invenio_campusonline.utils import (
    create_request_body_download,
    create_request_body_ids,
    create_request_body_metadata,
    create_request_header,
    get_embargo_range,
)


def test_create_request_body_metadata() -> None:
    """Test the create_request_body_metadata function."""
    body = create_request_body_metadata("abcd", "efgh")
    expected = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
      <soapenv:Header/>
      <soapenv:Body>
        <bas:getMetadataByThesisIDRequest>
          <bas:token>abcd</bas:token>
          <bas:ID>efgh</bas:ID>
          <bas:attr key="ALL"/>
          <bas:classAttrKeySet>
            <bas:name>text</bas:name>
            <bas:attr key="ALL"/>
          </bas:classAttrKeySet>
          <bas:classAttrKeySet>
            <bas:name>author</bas:name>
            <bas:attr key="ALL"/>
          </bas:classAttrKeySet>
          <bas:classAttrKeySet>
            <bas:name>supervisor</bas:name>
            <bas:attr key="ALL"/>
          </bas:classAttrKeySet>
        </bas:getMetadataByThesisIDRequest>
      </soapenv:Body>
    </soapenv:Envelope>
    """

    assert body == expected


def test_create_request_body_download() -> None:
    """Test the create_request_body_download function."""
    body = create_request_body_download("abcd", "efgh")
    expected = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
      <soapenv:Header/>
      <soapenv:Body>
        <bas:getDocumentByThesisIDRequest>
          <bas:token>abcd</bas:token>
          <bas:ID>efgh</bas:ID>
          <bas:docType>VOLLTEXT</bas:docType>
        </bas:getDocumentByThesisIDRequest>
      </soapenv:Body>
    </soapenv:Envelope>
    """
    assert body == expected


def test_create_request_body_ids() -> None:
    """Test the create_request_body_ids function."""
    body = create_request_body_ids("abcd", [])
    expected = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
      <soapenv:Header/>
      <soapenv:Body>
        <bas:getAllThesesMetadataRequest>
          <bas:token>abcd</bas:token>
          FILTER
        </bas:getAllThesesMetadataRequest>
      </soapenv:Body>
    </soapenv:Envelope>
    """.replace(
        "FILTER",
        "\n".join([]),
    )
    assert body == expected

    theses_filter = [
        """<bas:thesesType>DISS</bas:thesesType>""",
        """<bas:state name="IFG"/>""",
    ]
    body = create_request_body_ids("abcd", theses_filter)
    expected = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
      <soapenv:Header/>
      <soapenv:Body>
        <bas:getAllThesesMetadataRequest>
          <bas:token>abcd</bas:token>
          <bas:thesesType>DISS</bas:thesesType>
<bas:state name="IFG"/>
        </bas:getAllThesesMetadataRequest>
      </soapenv:Body>
    </soapenv:Envelope>
    """

    assert body == expected


def test_create_request_header() -> None:
    """Test the create_request_header function."""
    header = create_request_header("allThesesMetadataRequest")
    expected = {
        "Content-Type": "application/xml",
        "SOAPAction": "urn:service#allThesesMetadataRequest",
    }

    assert header == expected


def test_get_embargo_range(minimal_record: Element) -> None:
    """Test the get_embargo_range function."""
    embargo = get_embargo_range(minimal_record)

    assert embargo.end_date == "2025-03-03"
    assert bool(Embargo()) is False

    embargo = get_embargo_range(Element("root"))

    assert bool(embargo) is False

    if not bool(embargo := get_embargo_range(Element("root"))):
        assert bool(embargo) is False
