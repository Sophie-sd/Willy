"""JSON endpoints for Nova Poshta autocomplete on checkout."""

from __future__ import annotations

import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from orders.nova_poshta import (
    NovaPoshtaError,
    is_configured,
    search_cities,
    search_streets,
    search_warehouses,
)


def _json_error(message: str, status: int = 400):
    return JsonResponse({'ok': False, 'error': message, 'results': []}, status=status)


@require_GET
def np_cities(request):
    if not is_configured():
        return _json_error('Nova Poshta не налаштована на сервері', status=503)

    query = request.GET.get('q', '')
    try:
        results = search_cities(query)
    except NovaPoshtaError as exc:
        return _json_error(str(exc), status=502)
    return JsonResponse({'ok': True, 'results': results})


@require_GET
def np_warehouses(request):
    if not is_configured():
        return _json_error('Nova Poshta не налаштована на сервері', status=503)

    city_ref = request.GET.get('city_ref', '')
    query = request.GET.get('q', '')
    if not city_ref:
        return _json_error('Спочатку оберіть місто')
    try:
        results = search_warehouses(city_ref, query)
    except NovaPoshtaError as exc:
        return _json_error(str(exc), status=502)
    return JsonResponse({'ok': True, 'results': results})


@require_GET
def np_streets(request):
    if not is_configured():
        return _json_error('Nova Poshta не налаштована на сервері', status=503)

    settlement_ref = request.GET.get('settlement_ref', '')
    query = request.GET.get('q', '')
    if not settlement_ref:
        return _json_error('Спочатку оберіть місто')
    try:
        results = search_streets(settlement_ref, query)
    except NovaPoshtaError as exc:
        return _json_error(str(exc), status=502)
    return JsonResponse({'ok': True, 'results': results})
