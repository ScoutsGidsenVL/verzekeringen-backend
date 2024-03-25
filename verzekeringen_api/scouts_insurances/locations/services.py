import requests
from django.conf import settings


class BelgianPostalCodeCityService:
    endpoint = settings.BELGIAN_CITY_SEARCH_ENDPOINT

    def _get_dict(self, postal_code: str, city: str) -> dict:
        return {"postal_code": postal_code, "city": city}

    def search(self, term: str) -> list:
        payload = {"term": term}
        response = requests.get(self.endpoint, params=payload)

        response.raise_for_status()
        json = response.json()

        results = []
        for record in json:
            postal_code, city = record.split(" ", 1)
            results.append({"postal_code": postal_code, "city": city})

        return results

    def validate(self, postal_code: str, city: str) -> bool:
        """Validates a postal code against a city"""
        results = self.belgian_postcode_city_search(term=postal_code)
        for result in results:
            if result.city == city:
                return True
        return False
