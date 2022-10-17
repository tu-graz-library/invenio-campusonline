# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Command line interface to interact with the CampusOnline-Connector module."""

import xml.etree.ElementTree as ET

import click
from click_params import URL
from invenio_config_tugraz import get_identity_from_user_by_email
from invenio_records_marc21 import Marc21Metadata, create_record
from requests import post

from .convert import CampusOnlineToMarc21


def create_request_body(token, cms_id):
    """Build Request."""
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
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
</soapenv:Envelope>"""
    return body.replace("TOKEN", token).replace("CMS_ID", cms_id)


def create_request_header():
    headers = {
        "Content-Type": "application/xml",
        "SOAPAction": "urn:service#getMetadataByThesisID",
    }
    return headers


@click.group()
def campusonline():
    """CampusOnline CLI."""


@campusonline.command()
@click.option("--fetch-url", type=URL)
@click.option("--campusonline-id", type=click.STRING)
@click.option("--token", type=click.STRING)
@click.option("--user-email", type=click.STRING, default="cms@tugraz.at")
def fetch(fetch_url, campusonline_id, token):
    """Import records and files from campusonline"""
    body = create_request_body(token, campusonline_id)
    headers = create_request_header()
    response = post(fetch_url, data=body, headers=headers)

    root = ET.fromstring(response.text)

    convert = CampusOnlineToMarc21()
    marc21_record = Marc21Metadata()
    # thesis = root.find("")
    xpath = "{http://www.campusonline.at/thesisservice/basetypes}thesis"
    thesis = list(root.iter(xpath))[0]  # TODO: fix it

    convert.visit(thesis, marc21_record)
    identity = get_identity_from_user_by_email(email)

    record = create_record(marc21_record, file_path, identity)

    print(f"record.id: {record.id}")
