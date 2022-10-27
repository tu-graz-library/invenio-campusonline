# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.


"""Celery tasks for `invenio-campusonline`."""

import traceback

from celery import shared_task
from flask import current_app
from flask_mail import Message

from .utils import fetch_to_import_ids, import_from_campusonline


@shared_task(ignore_result=True)
def import_theses_from_campusonline():
    """Import theses from campusonline."""
    try:
        url = current_app.config["CAMPUSONLINE_URL"]
        token = current_app.config["CAMPUSONLINE_TOKEN"]
        user_email = current_app.config["CAMPUSONLINE_USER_EMAIL"]

        cms_ids = fetch_to_import_ids(url, token)

        for cms_id in cms_ids:
            import_from_campusonline(url, cms_id, token, user_email)
    except Exception:
        msg = Message(
            "Something went wrong when fetching data from moodle",
            sender=current_app.config["CAMPUSONLINE_ERROR_MAIL_SENDER"],
            recipients=current_app.config["CAMPUSONLINE_ERROR_MAIL_RECIPIENTS"],
            body=traceback.format_exc(),
        )
        current_app.extensions["mail"].send(msg)
