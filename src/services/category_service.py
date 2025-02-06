import time
from flask import current_app

from graph_db import GraphDB
from graph_builder import build_graph, get_graph_data
from wikipedia_fetcher import WikipediaFetcher

class CategoryService:
    def __init__(self, wikipedia_fetcher, graph_db):
        self.wikipedia = wikipedia_fetcher
        self.db = graph_db

    def process_category(self, category):
        page_titles = self.wikipedia.fetch_category_pages(category, limit=500)
        if not page_titles:
            raise ValueError(f"No pages found in category '{category}'")

        page_data = self._fetch_page_details(page_titles)
        graph = build_graph(page_data)
        
        self.db.load_graph(graph)
        graph_data = get_graph_data(graph)
        
        return {
            "message": "Graph generated and persisted successfully",
            "stats": {
                "nodes": graph.number_of_nodes(),
                "edges": graph.number_of_edges()
            },
            "graph_data": graph_data
        }

    def _fetch_page_details(self, page_titles):
        page_data = []
        for title in page_titles:
            details = self.wikipedia.fetch_page_details(title)
            if details:
                page_data.append(details)
            time.sleep(0.5)  # Respectful delay for the API
        return page_data 