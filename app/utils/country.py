class CountryCode:
    country_codes = {
        "IN": "India",
        "US": "United States",
        "GB": "United Kingdom",
        "CA": "Canada",
        "AU": "Australia",
        "DE": "Germany",
        "FR": "France",
        "JP": "Japan",
        "CN": "China",
        "BR": "Brazil",
        "ZA": "South Africa",
        "RU": "Russia",
        "IT": "Italy",
        "ES": "Spain",
        "MX": "Mexico",
        "KR": "South Korea",
        "NL": "Netherlands",
    }

    @classmethod
    def get_country_name(cls, code: str) -> str:
        return cls.country_codes.get(code.upper(), code)