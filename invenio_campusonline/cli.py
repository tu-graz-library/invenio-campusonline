# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Command line interface to interact with the CampusOnline-Connector module."""


from datetime import date as Date

from click import STRING, Choice, DateTime, group, option, secho
from click_params import URL
from flask import current_app
from flask.cli import with_appcontext

from .api import (
    duplicate_check_campusonline,
    fetch_all_ids,
    import_all_theses_from_campusonline,
    import_from_campusonline,
    set_status,
)
from .types import CampusOnlineConfigs, Color
from .utils import as_date


@group()
def campusonline() -> None:
    """Campusonline CLI."""


@campusonline.command()
@with_appcontext
@option("--endpoint", type=URL)
@option("--campusonline-id", type=STRING)
@option("--token", type=STRING)
@option("--user-email", type=STRING, default="cms@tugraz.at")
@option("--no-color", is_flag=True, default=False)
def import_thesis(
    endpoint: str,
    campusonline_id: str,
    token: str,
    user_email: str,
    no_color: bool,  # noqa: FBT001
) -> None:
    """Import metadata and file (aka one thesis) from campusonline."""
    import_func = current_app.config["CAMPUSONLINE_IMPORT_FUNC"]
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]
    recipients = current_app.config["CAMPUSONLINE_ERROR_MAIL_RECIPIENTS"]
    sender = current_app.config["CAMPUSONLINE_ERROR_MAIL_SENDER"]

    configs = CampusOnlineConfigs(
        endpoint,
        token,
        user_email,
        theses_filters,
        recipients,
        sender,
    )
    record = import_from_campusonline(import_func, campusonline_id, configs)

    color = Color.success if not no_color else Color.neutral
    secho(f"record.id: {record.id}", fg=color)


@campusonline.command()
@with_appcontext
@option("--endpoint", type=URL)
@option("--token", type=STRING)
@option("--no-color", is_flag=True, default=False)
def fetch_ids(
    endpoint: str,
    token: str,
    no_color: bool,  # noqa: FBT001
) -> None:
    """Fetch all to import ids."""
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]
    ids = fetch_all_ids(endpoint, token, theses_filters)

    color = Color.success if not no_color else Color.neutral
    secho(f"ids: {ids}", fg=color)


@campusonline.command()
@with_appcontext
@option("--endpoint", type=URL)
@option("--token", type=STRING)
@option("--user-email", type=STRING, default="cms@tugraz.at")
def full_sync(endpoint: str, token: str, user_email: str) -> None:
    """Full sync."""
    import_func = current_app.config["CAMPUSONLINE_IMPORT_FUNC"]
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]
    recipients = current_app.config["CAMPUSONLINE_ERROR_MAIL_RECIPIENTS"]
    sender = current_app.config["CAMPUSONLINE_ERROR_MAIL_SENDER"]

    configs = CampusOnlineConfigs(
        endpoint,
        token,
        user_email,
        theses_filters,
        recipients,
        sender,
    )
    import_all_theses_from_campusonline(import_func, configs)


@campusonline.command()
@with_appcontext
@option("--endpoint", type=URL, required=True)
@option("--token", type=STRING, required=True)
@option("--campusonline-id", type=STRING, default="")
def duplicate_check(endpoint: str, token: str, campusonline_id: str) -> None:
    """Duplicate check."""
    duplicate_func = current_app.config["CAMPUSONLINE_DUPLICATE_FUNC"]
    theses_filters = current_app.config["CAMPUSONLINE_THESES_FILTERS"]

    configs = CampusOnlineConfigs(
        endpoint,
        token,
        "",
        theses_filters,
        [],
        "",
    )
    duplicates = duplicate_check_campusonline(duplicate_func, configs, campusonline_id)

    for duplicate in duplicates:
        secho(duplicate, fg=Color.neutral)


@campusonline.command()
@with_appcontext
@option("--campusonline-id", type=STRING)
@option("--endpoint", type=URL)
@option("--token", type=STRING)
@option("--status", type=Choice(["ARCHIVED", "PUBLISHED"], case_sensitive=True))
@option("--date", type=DateTime(["%Y-%m-%d"]), callback=as_date)
@option("--no-color", is_flag=True, default=False)
def update_status(
    campusonline_id: str,
    endpoint: str,
    token: str,
    status: str,
    date: Date,
    no_color: bool,  # noqa: FBT001
) -> None:
    """Update status."""
    response = set_status(endpoint, token, campusonline_id, status, date)
    color = Color.success if not no_color else Color.neutral
    secho(f"response: {response}", fg=color)
