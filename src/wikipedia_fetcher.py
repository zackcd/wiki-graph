import requests
import time

class WikipediaFetcher:
    def __init__(self, api_url, api_token):
        self.api_url = api_url
        self.api_token = api_token

    def fetch_page_details(self, title):
        """
        Fetch details for a given Wikipedia page (title) including categories and links.
        Uses caching to avoid duplicate API calls.
        """
        # Caching removed since we're now using the graph DB for persistence.
        
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "categories|links",
            "cllimit": "max",
            "pllimit": "max"
        }

        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }


        response = requests.get(self.api_url, params=params, headers=headers)
        data = response.json()
        print(data)
        pages = data.get("query", {}).get("pages", {})
        for page_id, page in pages.items():
            # Skip pages that are categories themselves
            if title.startswith("Category:"):
                continue
            details = {
                "title": page.get("title"),
                "categories": [cat["title"] for cat in page.get("categories", [])] if "categories" in page else [],
                "links": [link["title"] for link in page.get("links", [])] if "links" in page else []
            }
            return details

        return None

    def fetch_sample_pages(self):
        """
        For demonstration, fetch a small list of pages.
        In practice, you would iterate over a more comprehensive list of pages.
        """
        sample_titles = [
            "Python (programming language)",
            "Java (programming language)",
            "C (programming language)"
        ]
        pages = []
        for title in sample_titles:
            details = self.fetch_page_details(title)
            if details:
                pages.append(details)
            time.sleep(1)  # Respectful delay for the API
        return pages

    def fetch_category_pages(self, category, limit=None):
        """
        Fetch pages in a given Wikipedia category using the MediaWiki API.
        """
        if not category.startswith("Category:"):
            category = "Category:" + category
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": limit if limit else "max",
            "format": "json"
        }
        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }
        response = requests.get(self.api_url, params=params, headers=headers)
        data = response.json()
        members = data.get("query", {}).get("categorymembers", [])
        # Extract page titles from members
        page_titles = [member["title"] for member in members]
        return page_titles 