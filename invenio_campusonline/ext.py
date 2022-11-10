# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""This module is used to import/export from/to the CampusOnline System."""

from . import config


class InvenioCampusonline(object):
    """invenio-campusonline extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-campusonline"] = self

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault("CELERY_BEAT_SCHEDULE", {})
        app.config.setdefault("INVENIO_MARC21_PERSISTENT_IDENTIFIER_PROVIDERS", [])
        app.config.setdefault("INVENIO_MARC21_PERSISTENT_IDENTIFIERS", {})

        for k in dir(config):
            if k == "CAMPUSONLINE_CELERY_BEAT_SCHEDULE":
                app.config["CELERY_BEAT_SCHEDULE"].update(getattr(config, k))
            elif k == "CAMPUSONLINE_PERSISTENT_IDENTIFIER_PROVIDERS":
                app.config["INVENIO_MARC21_PERSISTENT_IDENTIFIER_PROVIDERS"].extend(
                    getattr(config, k)
                )
            elif k == "CAMPUSONLINE_PERSISTENT_IDENTIFIERS":
                app.config["INVENIO_MARC21_PERSISTENT_IDENTIFIERS"].update(
                    getattr(config, k)
                )
            if k.startswith("CAMPUSONLINE_"):
                app.config.setdefault(k, getattr(config, k))
