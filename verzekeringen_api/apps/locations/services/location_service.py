import requests

from django.conf import settings

from apps.locations.utils import PostcodeCity


def belgian_postcode_city_search(term: str) -> list:
    payload = {"term": term}
    response = requests.get(settings.BELGIAN_CITY_SEARCH_ENDPOINT, params=payload)

    response.raise_for_status()
    json = response.json()

    results = []
    for record in json:
        postcode, name = record.split(" ", 1)
        results.append(PostcodeCity(postcode=postcode, name=name))

    return results


def validate_belgian_postcode_city(postcode: str, city_name: str) -> bool:
    results = belgian_postcode_city_search(term=postcode)
    for result in results:
        if result.name == city_name:
            return True
    return False
