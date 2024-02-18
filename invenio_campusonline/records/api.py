# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""API."""

from datetime import date as Date
from xml.etree.ElementTree import Element

from ..services import CampusOnlineRESTServiceConfig
from ..types import CampusOnlineID, CampusOnlineStatus, FilePath, ThesesFilter
from .models import CampusOnlineMetadata


def exists_fulltext(thesis: Element) -> bool:
    """Check against fulltext existens."""
    ns = "http://www.campusonline.at/thesisservice/basetypes"
    xpath = f".//{{{ns}}}document"
    ele = thesis.find(xpath)
    return ele is not None


class CampusOnlineRecord:
    """Campus online record."""

    model_cls = CampusOnlineMetadata

    def __init__(self, config: CampusOnlineRESTServiceConfig):
        self.model = self.model_cls(config)

    def fetch_ids(self, theses_filter: ThesesFilter) -> list:
        """Fetch ids."""
        root = self.model.post_ids(theses_filter)
        xpath = "{http://www.campusonline.at/thesisservice/basetypes}ID"
        return [CampusOnlineID(node.text) for node in root.iter(xpath)]

    def get_file_url(self, campusonline_id: CampusOnlineID) -> str:
        """Get file URL."""
        root = self.model.post_file_url(campusonline_id)

        if not exists_fulltext(root):
            msg = f"record ({campusonline_id}) has no associated file"
            raise RuntimeError(msg)

        xpath = "{http://www.campusonline.at/thesisservice/basetypes}docUrl"
        file_url = next(root.iter(xpath))

        return file_url.text

    def get_metadata(self, campusonline_id: CampusOnlineID) -> Element:
        """Get Metadata."""
        root = self.model.post_metadata(campusonline_id)

        xpath = "{http://www.campusonline.at/thesisservice/basetypes}thesis"
        return next(root.iter(xpath))

    def download_file(self, campusonline_id: CampusOnlineID) -> FilePath:
        """Download files from campus online by campusonline_id."""
        file_url = self.get_file_url(campusonline_id)

        file_path = f"/tmp/{campusonline_id}.pdf"  # noqa: S108
        self.model.store_file_temporarily(file_url, file_path)
        return file_path

    def set_status(
        self,
        cms_id: CampusOnlineID,
        status: CampusOnlineStatus,
        date: Date,
    ):
        """Set status."""
        return self.model.post_status(cms_id, status, date)
