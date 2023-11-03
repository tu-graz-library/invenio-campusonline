# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.

"""API functions of the campusonline connector."""

from collections.abc import Callable
from datetime import date as Date
from xml.etree.ElementTree import fromstring

from flask import current_app
from flask_mail import Message
from invenio_records_resources.services.records.results import RecordItem
from requests import post

from .types import (
    URL,
    CampusOnlineConfigs,
    CampusOnlineID,
    CampusOnlineStatus,
    CampusOnlineToken,
    ThesesFilter,
    ThesesState,
)
from .utils import (
    create_request_body_ids,
    create_request_body_status,
    create_request_header,
    download_file,
    get_metadata,
)


def import_from_campusonline(
    import_func: Callable,
    cms_id: CampusOnlineID,
    configs: CampusOnlineConfigs,
) -> RecordItem:
    """Import record from campusonline."""
    return import_func(cms_id, configs, get_metadata, download_file)


def fetch_all_ids(
    endpoint: URL,
    token: CampusOnlineToken,
    theses_filters: ThesesFilter = None,
) -> list[tuple[CampusOnlineID, ThesesState]]:
    """Fetch to import ids."""
    ids = []
    for theses_filter, state in theses_filters:
        body = create_request_body_ids(token, theses_filter)

        headers = create_request_header("getAllThesesMetadataRequest")
        response = post(endpoint, data=body, headers=headers, timeout=10)

        root = fromstring(response.text)
        xpath = "{http://www.campusonline.at/thesisservice/basetypes}ID"
        ids += [(CampusOnlineID(node.text), state) for node in root.iter(xpath)]

    return ids


def import_all_theses_from_campusonline(
    import_func: Callable,
    configs: CampusOnlineConfigs,
) -> None:
    """Import all theses from campusonline."""
    ids = fetch_all_ids(configs.endpoint, configs.token, configs.theses_filters)

    for cms_id, _ in ids:
        try:
            import_from_campusonline(import_func, cms_id, configs)
        except RuntimeError:
            msg = Message(
                "ERROR: importing from campusonline",
                sender=configs.sender,
                recipients=configs.recipients,
                body=f"thesis id: {cms_id}",
            )
            current_app.extensions["mail"].send(msg)


def duplicate_check_campusonline(
    duplicate_func: Callable,
    configs: CampusOnlineConfigs,
    campusonline_id: str,
) -> list:
    """Duplicate check campusonline."""
    if campusonline_id == "":
        ids = fetch_all_ids(configs.endpoint, configs.token, configs.theses_filters)
    else:
        ids = [(campusonline_id, "")]

    duplicates = []

    for cms_id, _ in ids:
        if duplicate_func(cms_id):
            duplicates.append(cms_id)

    return duplicates


def set_status(
    endpoint: URL,
    token: CampusOnlineToken,
    cms_id: CampusOnlineID,
    status: CampusOnlineStatus,
    date: Date,
) -> str:
    """Set status."""
    body = create_request_body_status(token, cms_id, status, date)
    headers = create_request_header("setThesisStatusByIDRequest")
    response = post(endpoint, data=body, headers=headers, timeout=10)
    return fromstring(response.text)
