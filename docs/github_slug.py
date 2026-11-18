"""Heading anchors that match GitHub's, so README links work on both sites."""

import re


def github_slug(title):
    """The anchor GitHub gives a heading: lowercase, punctuation dropped, spaces to hyphens."""
    return re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")
