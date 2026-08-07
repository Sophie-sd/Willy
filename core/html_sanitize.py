"""Sanitize HTML from TinyMCE / admin before storage and render."""

from __future__ import annotations

import nh3

ALLOWED_TAGS = frozenset({
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's',
    'ul', 'ol', 'li', 'a',
    'h2', 'h3', 'h4',
    'blockquote', 'span', 'div',
})

ALLOWED_ATTRIBUTES = {
    'a': {'href', 'title', 'target'},
}


def sanitize_html(value: str | None) -> str:
    if not value:
        return ''
    text = str(value).strip()
    if not text:
        return ''
    return nh3.clean(
        text,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        link_rel='noopener noreferrer',
    )
