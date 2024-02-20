# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Models."""

from datetime import date as Date
from pathlib import Path
from shutil import copyfileobj
from xml.etree.ElementTree import fromstring

from requests import get, post

from ..types import (
    URL,
    CampusOnlineID,
    CampusOnlineStatus,
    CampusOnlineToken,
    FilePath,
    ThesesFilter,
)


class CampusOnlineRESTPOSTXML:
    def __init__(self, token: CampusOnlineToken):
        self.token = token

    def create_request_body_status(
        self,
        campusonline_id: CampusOnlineID,
        status: CampusOnlineStatus,
        date: str,
    ) -> str:
        """Create request body status."""
        body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
          <soapenv:Header/>
          <soapenv:Body>
            <bas:setThesisStatusByIDRequest>
              <bas:token>{self.token}</bas:token>
              <bas:ID>{campusonline_id}</bas:ID>
              <bas:status>{status}</bas:status>
              <bas:statusDate>{date}</bas:statusDate>
            </bas:setThesisStatusByIDRequest>
          </soapenv:Body>
        </soapenv:Envelope>
        """
        return body

    def create_request_body_metadata(self, campusonline_id: CampusOnlineID) -> str:
        """Build Request."""
        body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
          <soapenv:Header/>
          <soapenv:Body>
            <bas:getMetadataByThesisIDRequest>
              <bas:token>{self.token}</bas:token>
              <bas:ID>{campusonline_id}</bas:ID>
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

        return body

    def create_request_body_download(self, campusonline_id: CampusOnlineID) -> str:
        """Build Request."""
        body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
          <soapenv:Header/>
          <soapenv:Body>
            <bas:getDocumentByThesisIDRequest>
              <bas:token>{self.token}</bas:token>
              <bas:ID>{campusonline_id}</bas:ID>
              <bas:docType>VOLLTEXT</bas:docType>
            </bas:getDocumentByThesisIDRequest>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        return body

    def create_request_body_ids(
        self,
        theses_filter: ThesesFilter,
    ) -> str:
        """Build request."""
        body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                          xmlns:bas="http://www.campusonline.at/thesisservice/basetypes">
          <soapenv:Header/>
          <soapenv:Body>
            <bas:getAllThesesMetadataRequest>
              <bas:token>{self.token}</bas:token>
              {str(theses_filter)}
            </bas:getAllThesesMetadataRequest>
          </soapenv:Body>
        </soapenv:Envelope>
        """

        return body

    @staticmethod
    def create_request_header(service: str) -> dict:
        """Create request header."""
        return {
            "Content-Type": "application/xml",
            "SOAPAction": f"urn:service#{service}",
        }


class CampusOnlineConnection:
    def __init__(self, config):
        self.config = config
        self.post_xml = CampusOnlineRESTPOSTXML(self.config.token)

    def post_ids(self, theses_filter):
        body = self.post_xml.create_request_body_ids(theses_filter)
        headers = self.post_xml.create_request_header("getAllThesesMetadataRequest")
        response = post(self.config.endpoint, data=body, headers=headers, timeout=10)

        return fromstring(response.text)

    def post_file_url(self, campusonline_id):
        body = self.post_xml.create_request_body_download(campusonline_id)
        headers = self.post_xml.create_request_header("getDocumentByThesisID")
        response = post(self.config.endpoint, data=body, headers=headers, timeout=10)

        return fromstring(response.text)

    def post_metadata(self, campusonline_id: CampusOnlineID):
        body = self.post_xml.create_request_body_metadata(campusonline_id)
        headers = self.post_xml.create_request_header("getMetadataByThesisID")
        response = post(self.config.endpoint, data=body, headers=headers, timeout=10)

        return fromstring(response.text)

    def store_file_temporarily(self, file_url: URL, file_path: FilePath) -> None:
        """Store the file referenced by url to the local file path."""
        file_url = f"{file_url}{self.config.token}"
        with get(file_url, stream=True, timeout=10) as response:
            with Path(file_path).open("wb") as fp:
                copyfileobj(response.raw, fp)

    def post_status(
        self,
        cms_id: CampusOnlineID,
        status: CampusOnlineStatus,
        date: Date,
    ):
        """Post status."""
        body = self.post_xml.create_request_body_status(cms_id, status, date)
        headers = self.post_xml.create_request_header("setThesisStatusByIDRequest")
        response = post(self.config.endpoint, data=body, headers=headers, timeout=10)
        return fromstring(response.text)
