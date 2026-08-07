"""Honeypot login at /admin/ — logs attempts, never authenticates."""

from __future__ import annotations

import re

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from core.models import AdminLoginAttempt


def _client_ip(request) -> str | None:
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()[:45] or None
    return (request.META.get('REMOTE_ADDR') or '').strip()[:45] or None


def _device_summary(user_agent: str) -> str:
    ua = user_agent or ''
    parts = []

    if re.search(r'iPhone|iPad|iPod', ua, re.I):
        parts.append('iOS')
    elif re.search(r'Android', ua, re.I):
        parts.append('Android')
    elif re.search(r'Windows', ua, re.I):
        parts.append('Windows')
    elif re.search(r'Mac OS X|Macintosh', ua, re.I):
        parts.append('macOS')
    elif re.search(r'Linux', ua, re.I):
        parts.append('Linux')

    if re.search(r'Edg/', ua):
        parts.append('Edge')
    elif re.search(r'OPR/|Opera', ua, re.I):
        parts.append('Opera')
    elif re.search(r'Chrome/', ua) and 'Chromium' not in ua:
        parts.append('Chrome')
    elif re.search(r'Safari/', ua) and 'Chrome' not in ua:
        parts.append('Safari')
    elif re.search(r'Firefox/', ua):
        parts.append('Firefox')
    elif re.search(r'bot|crawler|spider|curl|wget|python-requests', ua, re.I):
        parts.append('Bot/скрипт')

    if re.search(r'Mobile', ua, re.I) and 'iOS' not in parts and 'Android' not in parts:
        parts.append('Mobile')

    return ', '.join(parts) if parts else 'Невідомий пристрій'


def _log_attempt(request) -> None:
    username = (request.POST.get('username') or '')[:150]
    password = request.POST.get('password') or ''
    user_agent = (request.META.get('HTTP_USER_AGENT') or '')[:2000]
    AdminLoginAttempt.objects.create(
        username=username,
        password_length=min(len(password), 255),
        ip_address=_client_ip(request),
        user_agent=user_agent,
        device_summary=_device_summary(user_agent)[:255],
        accept_language=(request.META.get('HTTP_ACCEPT_LANGUAGE') or '')[:128],
        referer=(request.META.get('HTTP_REFERER') or '')[:512],
        path=request.path[:255],
    )


@ensure_csrf_cookie
@require_http_methods(['GET', 'POST', 'HEAD'])
def admin_honeypot(request):
    if request.method == 'POST':
        try:
            _log_attempt(request)
        except Exception:
            # Never reveal failures to the visitor
            pass

    return render(request, 'honeypot/admin_login.html', {
        'title': 'Увійти | Адміністрування сайту',
    })
