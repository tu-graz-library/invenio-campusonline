# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.


"""Celery tasks for `invenio-campusonline`."""

from celery import shared_task
from flask import current_app
from flask_mail import Message

from .api import fetch_all_ids, import_from_campusonline


def config_variables():
    """Configuration variables."""
    url = current_app.config["CAMPUSONLINE_ENDPOINT"]
    token = current_app.config["CAMPUSONLINE_TOKEN"]
    user_email = current_app.config["CAMPUSONLINE_USER_EMAIL"]
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]
    recipients = ",".join(current_app.config["CAMPUSONLINE_ERROR_MAIL_RECIPIENTS"])
    sender = current_app.config["CAMPUSONLINE_ERROR_MAIL_SENDER"]

    return url, token, user_email, theses_filters, recipients, sender


@shared_task(ignore_result=True)
def import_theses_from_campusonline():
    """Import theses from campusonline."""
    url, token, user_email, theses_filters, recipients, sender = config_variables()
    cms_ids = fetch_all_ids(url, token, theses_filters)

    for cms_id in cms_ids:
        try:
            import_from_campusonline(url, cms_id, token, user_email)
        except Exception:
            msg = Message(
                "ERROR: importing from campusonline",
                sender=sender,
                recipients=recipients,
                body=f"thesis id: {cms_id}",
            )
            current_app.extensions["mail"].send(msg)
