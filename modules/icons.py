"""
Lightweight inline-SVG icon set.

Pure presentation helper — returns HTML strings only. Does not touch
session state, storage, or any backend logic. Safe to import anywhere
that already renders unsafe_allow_html markdown.
"""

_PATHS = {
    "home": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M9.5 21v-6h5v6"/>',
    "dashboard": '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17.5" cy="9" r="2.5"/><path d="M15.8 14.2c2.6.4 4.7 2.6 4.7 5.8"/>',
    "user": '<circle cx="12" cy="8" r="3.6"/><path d="M4.5 20c0-4.1 3.4-7.5 7.5-7.5s7.5 3.4 7.5 7.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.2"/><path d="m3.5 6 8.5 7 8.5-7"/>',
    "phone": '<path d="M6.6 3.5 9.5 6.4c.4.4.4 1 .1 1.5L8 10.4c1.1 2.6 3 4.5 5.6 5.6l2.5-1.6c.4-.3 1.1-.3 1.5.1l2.9 2.9c.5.5.5 1.4-.1 1.9-1 1-2.4 1.5-3.8 1.3-6-.9-10.8-5.7-11.7-11.7-.2-1.4.3-2.8 1.3-3.8.5-.6 1.4-.6 1.9-.1Z"/>',
    "link": '<path d="M9.5 14.5 14.5 9.5"/><path d="M11 6l1.4-1.4a3.5 3.5 0 0 1 5 5L16 11"/><path d="M13 18l-1.4 1.4a3.5 3.5 0 0 1-5-5L8 13"/>',
    "award": '<circle cx="12" cy="8.5" r="5"/><path d="M9 12.8 7.5 21l4.5-2.5 4.5 2.5-1.5-8.2"/>',
    "trending": '<path d="m3.5 17 6-6.5 4 4L20.5 6"/><path d="M15 6h5.5v5.5"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m20 20-4.6-4.6"/>',
    "upload": '<path d="M12 15.5V4"/><path d="m7 8.5 5-5 5 5"/><path d="M4.5 15v3.2A2.3 2.3 0 0 0 6.8 20.5h10.4a2.3 2.3 0 0 0 2.3-2.3V15"/>',
    "file": '<path d="M6.5 2.5h8l4 4v14.5a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1Z"/><path d="M14 2.5V7a1 1 0 0 0 1 1h4.5"/><path d="M9 13h6M9 16.5h6"/>',
    "sparkles": '<path d="M12 3.5 13.4 8l4.6 1.4-4.6 1.4L12 15.2l-1.4-4.4L6 9.4 10.6 8Z"/><path d="M19 15.5l.8 2.1 2.2.8-2.2.8-.8 2.1-.8-2.1-2.2-.8 2.2-.8Z"/>',
    "download": '<path d="M12 3.5V15"/><path d="m7 10.5 5 5 5-5"/><path d="M4.5 18.5V20a1.5 1.5 0 0 0 1.5 1.5h12a1.5 1.5 0 0 0 1.5-1.5v-1.5"/>',
    "check": '<path d="m4.5 12.5 5 5 10-10.5"/>',
    "cross": '<path d="M6 6l12 12M18 6 6 18"/>',
    "briefcase": '<rect x="3" y="7.5" width="18" height="12" rx="2"/><path d="M8.5 7.5V6a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v1.5"/><path d="M3 13h18"/>',
    "layers": '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 16 9 5 9-5"/>',
    "shield": '<path d="M12 3 5 6v5.5c0 4.4 3 7.9 7 9 4-1.1 7-4.6 7-9V6l-7-3Z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    "logout": '<path d="M9 4.5H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h3"/><path d="M15.5 16l4-4-4-4"/><path d="M19 12H9"/>',
    "star": '<path d="m12 3 2.7 5.7 6.3.6-4.7 4.2 1.3 6.2L12 16.8 6.4 19.7l1.3-6.2-4.7-4.2 6.3-.6Z"/>',
    "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="0.6" fill="currentColor" stroke="none"/>',
    "zap": '<path d="M12.5 2.5 4.5 14h6l-1 7.5 8-11.5h-6Z"/>',
    "chart": '<path d="M4 20V10M11 20V4M18 20v-7"/>',
    "check-shield": '<path d="M12 3 5 6v5.5c0 4.4 3 7.9 7 9 4-1.1 7-4.6 7-9V6l-7-3Z"/>',
    "arrow-right": '<path d="M4.5 12h15"/><path d="m13 5.5 6.5 6.5-6.5 6.5"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/>',
    "id": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><circle cx="8.5" cy="12" r="2.2"/><path d="M6 16.3c.4-1.6 1.6-2.5 2.5-2.5s2.1.9 2.5 2.5"/><path d="M14.5 9.5h4M14.5 12.5h4M14.5 15.5h2.5"/>',
    "database": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/><path d="M4.5 5.5V18c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8V5.5"/><path d="M4.5 11.8c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/>',
    "clipboard-check": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v1"/><path d="m8.5 13 2.3 2.3L15.5 11"/>',
}


def svg(name, size=18, stroke_width=2, color="currentColor"):
    """Return an inline <svg> string for the given icon name."""

    body = _PATHS.get(name, _PATHS["star"])

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-3px;flex-shrink:0;">'
        f'{body}</svg>'
    )


def icon_tile(name, size=18, tone="brand"):
    """A small rounded icon chip, used for feature/metric card headers."""

    return (
        f'<span class="icon-tile icon-tile-{tone}">{svg(name, size=size)}</span>'
    )
