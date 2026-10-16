# SPDX-FileCopyrightText: 2025-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Jobs for invenio-campusonline."""

from invenio_jobs.jobs import JobType

from .tasks import import_theses_from_campusonline


class ImportThesesFromCampusonlineJob(JobType):
    """Import theses from campusonline."""

    id = "import_theses_from_campusonline"
    title = "Import theses from campusonline"
    description = "Import theses from campusonline"

    task = import_theses_from_campusonline
