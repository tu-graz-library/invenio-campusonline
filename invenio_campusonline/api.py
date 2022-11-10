# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.

"""API functions of the campusonline connector."""

from xml.etree.ElementTree import fromstring

from invenio_config_tugraz import get_identity_from_user_by_email
from invenio_records_marc21 import Marc21Metadata, create_record, current_records_marc21
from requests import post

from .convert import CampusOnlineToMarc21
from .utils import (
    create_request_body_ids,
    create_request_header,
    download_file,
    get_file_url,
    get_metadata,
)


def import_from_campusonline(endpoint, campusonline_id, token, user_email):
    """Import record from campusonline."""
    thesis = get_metadata(endpoint, token, campusonline_id)
    convert = CampusOnlineToMarc21()
    marc21_record = Marc21Metadata()

    convert.visit(thesis, marc21_record)
    file_url = get_file_url(endpoint, token, campusonline_id)
    file_path = f"/tmp/{campusonline_id}.pdf"  # TODO add author name
    download_file(token, file_url, file_path)

    identity = get_identity_from_user_by_email(email=user_email)
    service = current_records_marc21.records_service
    record = create_record(service, marc21_record, file_path, identity)
    return record


def fetch_all_ids(endpoint, token, theses_filter=None):
    """Fetch to import ids."""
    body = create_request_body_ids(token, theses_filter)
    headers = create_request_header("getAllThesesMetadataRequest")
    response = post(endpoint, data=body, headers=headers)

    root = fromstring(response.text)
    xpath = "{http://www.campusonline.at/thesisservice/basetypes}ID"
    ids = [node.text for node in root.iter(xpath)]
    return ids
