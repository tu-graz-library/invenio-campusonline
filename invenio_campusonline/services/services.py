# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Services."""


from datetime import date as Date

from flask_principal import Identity

from ..records import CampusOnlineAPI
from ..types import CampusOnlineID, CampusOnlineStatus, ThesesFilter
from .config import CampusOnlineRESTServiceConfig


class CampusOnlineRESTService:
    """Campusonline REST service."""

    def __init__(self, config: CampusOnlineRESTServiceConfig) -> None:
        """Construct."""
        self._config = config
        self.api = self.api_cls(config=config)

    @property
    def api_cls(self) -> CampusOnlineAPI:
        """Get api cls."""
        return self._config.api_cls

    def fetch_all_ids(self, identity: Identity, theses_filter: ThesesFilter):
        """Fetch all ids."""
        # self.require_permission()
        return self.api.fetch_ids(theses_filter)

    def download_file(self, identity: Identity, cms_id: CampusOnlineID):
        """Download file."""
        # self.require_permission()
        return self.api.download_file(cms_id)

    def get_metadata(self, identity: Identity, cms_id: CampusOnlineID):
        """Get metadata."""
        # self.require_permission()
        return self.api.get_metadata(cms_id)

    def set_status(
        self,
        identity: Identity,
        cms_id: CampusOnlineID,
        status: CampusOnlineStatus,
        date: Date,
    ):
        """Set Status."""
        # self.require_permission()
        self.api.set_status(cms_id, status, date)
