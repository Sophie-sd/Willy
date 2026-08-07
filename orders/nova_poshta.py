"""Nova Poshta API v2.0 client (cities, warehouses, streets)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

API_URL = 'https://api.novaposhta.ua/v2.0/json/'

_API_KEY_ENV_NAMES = (
    'NOVA_POSHTA_API_KEY',
    'NP_API_KEY',
    'NOVA_POSHTA_TOKEN',
)


class NovaPoshtaError(Exception):
    pass


def get_api_key() -> str:
    for name in _API_KEY_ENV_NAMES:
        value = os.environ.get(name, '').strip()
        if value:
            return value
    return ''


def is_configured() -> bool:
    return bool(get_api_key())


def _request(model_name: str, called_method: str, method_properties: dict) -> list:
    api_key = get_api_key()
    if not api_key:
        raise NovaPoshtaError(
            'API-ключ Нової Пошти не задано. '
            'Додайте NOVA_POSHTA_API_KEY у .env',
        )

    payload = {
        'apiKey': api_key,
        'modelName': model_name,
        'calledMethod': called_method,
        'methodProperties': method_properties,
    }
    body = json.dumps(payload).encode('utf-8')
    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='replace')[:200]
        raise NovaPoshtaError(f'Nova Poshta HTTP {exc.code}: {detail}') from exc
    except urllib.error.URLError as exc:
        raise NovaPoshtaError(f'Nova Poshta мережа: {exc.reason}') from exc
    except json.JSONDecodeError as exc:
        raise NovaPoshtaError('Некоректна відповідь Nova Poshta') from exc

    if not data.get('success'):
        errors = data.get('errors') or data.get('errorCodes') or ['Невідома помилка']
        raise NovaPoshtaError('; '.join(str(item) for item in errors))

    return data.get('data') or []


def search_cities(query: str, *, limit: int = 20) -> list[dict]:
    query = (query or '').strip()
    if len(query) < 2:
        return []

    rows = _request('Address', 'searchSettlements', {
        'CityName': query,
        'Limit': str(limit),
    })
    results = []
    for block in rows:
        for item in block.get('Addresses') or []:
            present = (item.get('Present') or '').strip()
            main = (item.get('MainDescription') or '').strip()
            settlement_ref = (item.get('Ref') or '').strip()
            city_ref = (item.get('DeliveryCity') or '').strip()
            if not present or not settlement_ref:
                continue
            results.append({
                'label': present,
                'city': main or present,
                'settlement_ref': settlement_ref,
                'city_ref': city_ref or settlement_ref,
            })
    return results


def search_warehouses(city_ref: str, query: str = '', *, limit: int = 50) -> list[dict]:
    city_ref = (city_ref or '').strip()
    if not city_ref:
        return []

    props = {
        'CityRef': city_ref,
        'Limit': str(limit),
        'Page': '1',
    }
    query = (query or '').strip()
    if query:
        props['FindByString'] = query

    rows = _request('Address', 'getWarehouses', props)
    results = []
    for item in rows:
        description = (item.get('Description') or item.get('DescriptionRu') or '').strip()
        ref = (item.get('Ref') or '').strip()
        if not description or not ref:
            continue
        results.append({
            'label': description,
            'ref': ref,
            'number': (item.get('Number') or '').strip(),
        })
    return results


def search_streets(settlement_ref: str, query: str, *, limit: int = 30) -> list[dict]:
    settlement_ref = (settlement_ref or '').strip()
    query = (query or '').strip()
    if not settlement_ref or len(query) < 2:
        return []

    rows = _request('Address', 'searchSettlementStreets', {
        'StreetName': query,
        'SettlementRef': settlement_ref,
        'Limit': str(limit),
    })
    results = []
    for block in rows:
        for item in block.get('Addresses') or []:
            present = (item.get('Present') or '').strip()
            ref = (item.get('SettlementStreetRef') or item.get('Ref') or '').strip()
            if not present:
                continue
            results.append({
                'label': present,
                'ref': ref,
            })
    return results
