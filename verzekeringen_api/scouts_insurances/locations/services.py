import json
import re
import requests

from django.conf import settings
from django.core.cache import cache


class BelgianPostalCodeCityService:
    endpoint = settings.BELGIAN_CITY_SEARCH_ENDPOINT

    def _get_dict(self, postal_code: str, city: str) -> dict:
        return {"postal_code": postal_code, "city": city}

    def _search(self, term: str) -> list:
        payload = {"term": term}
        response = requests.get(re.sub("^https:http:", "https:", self.endpoint), params=payload)

        response.raise_for_status()
        json = response.json()

        results = []
        for record in json:
            postal_code, city = record.split(" ", 1)
            results.append({"postal_code": postal_code, "city": city})

        return results

    def search(self, term: str) -> list:
        """Search and filter with cached data first, if not found, search the API.
        This method will never cache itself.
        """
        if not term:
            return self.fetch_all()

        cache_key = "belgian_postal_codes"
        json_data = cache.get(cache_key)
        if json_data:
            data = json_data.loads(json_data)
            filtered = [result for result in data if term in result["postal_code"] or term in result["city"]]
            return filtered
        return self._search(term)

    def _fetch_all(self) -> list:
        """Searches all data from the API by searching with terms 1-9."""
        results = []
        for i in range(1, 10):
            results.append(self._search(str(i)))

        # Flatten array and keep uniques only.
        return [item for sublist in results for item in sublist]

    def fetch_all(self) -> list:
        """Fetch all data and cache it if not already cached."""
        cache_key = "belgian_postal_codes"
        json_data = cache.get(cache_key)
        if json_data:
            data = json.loads(json_data)
        else:
            data = self._fetch_all()
            json_data = json.dumps(data)
            cache.set(cache_key, json_data)
        return data
