# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Command line interface to interact with the CampusOnline-Connector module."""

import xml.etree.ElementTree as ET
from shutil import copyfileobj

import click
from click_params import URL
from flask.cli import with_appcontext
from invenio_config_tugraz import get_identity_from_user_by_email
from invenio_records_marc21 import Marc21Metadata, create_record, current_records_marc21
from requests import get, post

from .convert import CampusOnlineToMarc21


def create_request_body_metadata(token, cms_id):
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


def create_request_body_download(token, cms_id):
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


def create_request_header(service):
    """Create request header."""
    headers = {
        "Content-Type": "application/xml",
        "SOAPAction": f"urn:service#{service}",
    }
    return headers


def get_metadata(fetch_url, token, campusonline_id):
    """Get Metadata."""
    body = create_request_body_metadata(token, campusonline_id)
    headers = create_request_header("getMetadataByThesisID")
    response = post(fetch_url, data=body, headers=headers)

    root = ET.fromstring(response.text)

    # thesis = root.find("")
    xpath = "{http://www.campusonline.at/thesisservice/basetypes}thesis"
    thesis = list(root.iter(xpath))[0]  # TODO: fix it
    return thesis


def get_file_url(fetch_url, token, campusonline_id):
    """Get file URL."""
    body = create_request_body_download(token, campusonline_id)
    headers = create_request_header("getDocumentByThesisID")
    response = post(fetch_url, data=body, headers=headers)

    root = ET.fromstring(response.text)

    xpath = "{http://www.campusonline.at/thesisservice/basetypes}docUrl"
    file_url = list(root.iter(xpath))[0]  # TODO: make it more nice
    return file_url.text


def download_file(token, file_url, file_path):
    """Download file."""
    file_url = f"{file_url}{token}"
    with get(file_url, stream=True) as response:
        with open(file_path, "wb") as fp:
            copyfileobj(response.raw, fp)


@click.group()
def campusonline():
    """CampusOnline CLI."""


@campusonline.command()
@with_appcontext
@click.option("--fetch-url", type=URL)
@click.option("--campusonline-id", type=click.STRING)
@click.option("--token", type=click.STRING)
@click.option("--user-email", type=click.STRING, default="cms@tugraz.at")
def fetch(fetch_url, campusonline_id, token, user_email):
    """Import records and files from campusonline"""

    thesis = get_metadata(fetch_url, token, campusonline_id)
    convert = CampusOnlineToMarc21()
    marc21_record = Marc21Metadata()

    convert.visit(thesis, marc21_record)
    file_url = get_file_url(fetch_url, token, campusonline_id)
    file_path = f"/tmp/{campusonline_id}.pdf"  # TODO add author name
    download_file(token, file_url, file_path)

    identity = get_identity_from_user_by_email(email=user_email)
    service = current_records_marc21.records_service
    record = create_record(service, marc21_record, file_path, identity)

    print(f"record.id: {record.id}")
