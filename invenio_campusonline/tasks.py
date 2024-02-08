# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2024 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.


"""Celery tasks for `invenio-campusonline`."""


from celery import shared_task
from flask import current_app

from .api import import_all_theses_from_campusonline
from .utils import config_variables


@shared_task(ignore_result=True)
def import_theses_from_campusonline() -> None:
    """Import theses from campusonline."""
    import_func = current_app.config["CAMPUSONLINE_IMPORT_FUNC"]
    configs = config_variables()
    import_all_theses_from_campusonline(import_func, configs)
