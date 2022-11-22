# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.

"""Command line interface to interact with the CampusOnline-Connector module."""

from shutil import copyfileobj
from xml.etree.ElementTree import Element, fromstring

from requests import get, post

from .types import CampusOnlineId


def create_request_body_metadata(token: str, cms_id: str):
    """Build Request."""
    body = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
      <soapenv:Header/>
      <soapenv:Body>
        <bas:getMetadataByThesisIDRequest>
          <bas:token>TOKEN</bas:token>
          <bas:ID>CMS_ID</bas:ID>
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

    return body.replace("TOKEN", token).replace("CMS_ID", cms_id)


def create_request_body_download(token: str, cms_id: str):
    """Build Request."""
    body = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
      <soapenv:Header/>
      <soapenv:Body>
        <bas:getDocumentByThesisIDRequest>
          <bas:token>TOKEN</bas:token>
          <bas:ID>CMS_ID</bas:ID>
          <bas:docType>VOLLTEXT</bas:docType>
        </bas:getDocumentByThesisIDRequest>
      </soapenv:Body>
    </soapenv:Envelope>
    """

    return body.replace("TOKEN", token).replace("CMS_ID", cms_id)


def create_request_body_ids(token: str, theses_filter: list[Element] = None):
    """Build request."""
    body = """
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
      <soapenv:Header/>
      <soapenv:Body>
        <bas:getAllThesesMetadataRequest>
          <bas:token>TOKEN</bas:token>
          FILTER
        </bas:getAllThesesMetadataRequest>
      </soapenv:Body>
    </soapenv:Envelope>
    """

    default_theses_filter = [
        """<bas:thesesType>DIPLARB</bas:thesesType>""",
        """<bas:state name="IFG"/>""",
    ]
    theses_filter = theses_filter if theses_filter else default_theses_filter
    return body.replace("TOKEN", token).replace("FILTER", "\n".join(theses_filter))


def create_request_header(service: str):
    """Create request header."""
    header = {
        "Content-Type": "application/xml",
        "SOAPAction": f"urn:service#{service}",
    }
    return header


def get_metadata(endpoint: str, token: str, campusonline_id: CampusOnlineId):
    """Get Metadata."""
    body = create_request_body_metadata(token, campusonline_id.cms_id)
    headers = create_request_header("getMetadataByThesisID")
    response = post(endpoint, data=body, headers=headers)

    root = fromstring(response.text)

    xpath = "{http://www.campusonline.at/thesisservice/basetypes}thesis"
    thesis = list(root.iter(xpath))[0]  # TODO: fix it
    return thesis


def get_file_url(endpoint: str, token: str, campusonline_id: CampusOnlineId):
    """Get file URL."""
    body = create_request_body_download(token, campusonline_id.cms_id)
    headers = create_request_header("getDocumentByThesisID")
    response = post(endpoint, data=body, headers=headers)

    root = fromstring(response.text)
    xpath = "{http://www.campusonline.at/thesisservice/basetypes}docUrl"
    file_url = list(root.iter(xpath))[0]  # TODO: make it more nice
    return file_url.text


def download_file(token: str, file_url: str, file_path: str):
    """Download file."""
    file_url = f"{file_url}{token}"
    with get(file_url, stream=True) as response:
        with open(file_path, "wb") as fp:
            copyfileobj(response.raw, fp)
