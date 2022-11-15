# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""This is the configuration file."""

from invenio_rdm_records.services.pids import providers

CAMPUSONLINE_ENDPOINT = ""
"""This is the endpoint to fetch the records."""

CAMPUSONLINE_TOKEN = ""
"""This is the token to get the records from the campusonline endpoint."""

CAMPUSONLINE_USER_EMAIL = ""
"""This is the email adress of the campusonline user in the repository."""

CAMPUSONLINE_ERROR_MAIL_SENDER = ""
"""This is the error mail sender."""

CAMPUSONLINE_ERROR_MAIL_RECIPIENTS = []
"""This is the email adress to send error messages to be fixed in the repository."""

CAMPUSONLINE_THESES_FILTER = []
"""This filter provides the possibiliy to set filters for the fetched theses."""

CAMPUSONLINE_CELERY_BEAT_SCHEDULE = {}
"""Celery beat schedule for the theses import."""

CAMPUSONLINE_PERSISTENT_IDENTIFIER_PROVIDERS = [
    providers.ExternalPIDProvider(
        "campusonline", "campusonline", label="CAMPUSONLINE ID"
    )
]
"""Persistent identifier provider for campusonline."""

CAMPUSONLINE_PERSISTENT_IDENTIFIERS = {
    "campusonline": {
        "providers": ["campusonline"],
        "required": False,
        "label": "CAMPUSONLINE",
    }
}
"""Persistent identifiers for campusonline."""
