# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""The module is used to import/export from/to the CampusOnline System."""

from flask import Flask

from .services import CampusOnlineRESTService, CampusOnlineRESTServiceConfig


class InvenioCampusonline:
    """invenio-campusonline extension."""

    def __init__(self, app: Flask = None) -> None:
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Flask application initialization."""
        self.init_services(app)
        app.extensions["invenio-campusonline"] = self

    def init_services(self, app: Flask) -> None:
        """Initialize services."""
        endpoint = app.config.get("CAMPUSONLINE_ENDPOINT", "")
        token = app.config.get("CAMPUSONLINE_TOKEN", "")
        config = CampusOnlineRESTServiceConfig(endpoint, token)
        self.campusonline_rest_service = CampusOnlineRESTService(config)
