# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Services."""


from collections.abc import Callable
from datetime import date as Date
from datetime import datetime
from functools import wraps
from typing import Any
from xml.etree.ElementTree import Element

from flask_principal import Identity

from ..records import CampusOnlineAPI
from ..types import CampusOnlineID, CampusOnlineStatus, Embargo, ThesesFilter
from .config import CampusOnlineRESTServiceConfig


def build_services(f: Callable) -> Callable:
    """Decorate to build the services."""

    @wraps(f)
    def build(*_: dict, **kwargs: dict) -> Any:  # noqa: ANN401
        endpoint = kwargs.pop("endpoint")
        token = kwargs.pop("token")

        config = CampusOnlineRESTServiceConfig(endpoint, token)
        kwargs["cms_service"] = CampusOnlineRESTService(config)

        return f(**kwargs)

    return build


class CampusOnlineRESTService:
    """Campusonline REST service."""

    api_cls = CampusOnlineAPI

    def __init__(self, config: CampusOnlineRESTServiceConfig) -> None:
        """Construct."""
        self._config = config
        self.api = self.api_cls(config=config)

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
