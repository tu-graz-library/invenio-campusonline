# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Command line interface to interact with the CampusOnline-Connector module."""

import click


@click.group()
def campusonline():
    """CampusOnline CLI."""


@campusonline.command()
def fetch():
    """Import records and files from campusonline"""
    pass
