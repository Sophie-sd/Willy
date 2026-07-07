import json
import os
import urllib.error
import urllib.request

PLACE_SEARCH_QUERY = 'ЗООМАГАЗИН Willi Академмістечко, проспект Академіка Палладіна 23а, Київ'
PLACE_FIELDS = 'id,reviews,rating,userRatingCount,displayName'


def _api_request(url, *, method='GET', data=None, field_mask=None):
    api_key = os.environ.get('GOOGLE_PLACES_API_KEY', '').strip()
    if not api_key:
        return None, 'GOOGLE_PLACES_API_KEY не задано в .env'

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
    }
    if field_mask:
        headers['X-Goog-FieldMask'] = field_mask

    body = json.dumps(data).encode('utf-8') if data is not None else None
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode('utf-8'))
            return payload, None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='replace')
        return None, f'Google Places API: {exc.code} {detail[:300]}'
    except urllib.error.URLError as exc:
        return None, f'Google Places API: {exc.reason}'


def find_place_id(query=PLACE_SEARCH_QUERY):
    payload, error = _api_request(
        'https://places.googleapis.com/v1/places:searchText',
        method='POST',
        data={'textQuery': query, 'languageCode': 'uk'},
        field_mask='places.id,places.displayName',
    )
    if error:
        return None, error

    places = payload.get('places') or []
    if not places:
        return None, 'Магазин не знайдено в Google Places API'

    place_id = places[0]['id']
    if place_id.startswith('places/'):
        place_id = place_id.removeprefix('places/')
    return place_id, None


def fetch_place_reviews(place_id):
    payload, error = _api_request(
        f'https://places.googleapis.com/v1/places/{place_id}',
        field_mask=PLACE_FIELDS,
    )
    if error:
        return None, error

    reviews = []
    for item in payload.get('reviews') or []:
        text = (item.get('text') or {}).get('text', '').strip()
        author = (item.get('authorAttribution') or {}).get('displayName', '').strip()
        rating = item.get('rating') or 5
        review_id = (item.get('name') or '').strip()
        if not text or not author:
            continue
        reviews.append({
            'google_review_id': review_id,
            'text': text,
            'author': author,
            'rating': int(rating),
        })
    return {
        'place_id': place_id,
        'rating': payload.get('rating'),
        'user_rating_count': payload.get('userRatingCount'),
        'reviews': reviews,
    }, None
