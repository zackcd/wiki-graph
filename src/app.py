#!/usr/bin/env python3
import os
from flask import Flask
from services.category_service import CategoryService
from wikipedia_fetcher import WikipediaFetcher
from graph_db import GraphDB

def create_app():
    app = Flask(__name__)

    # Move configuration to environment variables or config file
    app.config.update(
        WIKIPEDIA_API_URL="https://en.wikipedia.org/w/api.php",
        NEO4J_URI=os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
        NEO4J_USER=os.environ.get("NEO4J_USER", "neo4j"),
        NEO4J_PASSWORD=os.environ.get("NEO4J_PASSWORD", "test")
    )

    # Initialize dependencies
    wikipedia_fetcher = WikipediaFetcher(app.config['WIKIPEDIA_API_URL'], app.config['WIKIPEDIA_API_TOKEN'])
    graph_db = GraphDB(
        app.config['NEO4J_URI'],
        app.config['NEO4J_USER'],
        app.config['NEO4J_PASSWORD']
    )

    # Initialize services with dependencies
    app.category_service = CategoryService(wikipedia_fetcher, graph_db)
    
    # Register blueprints
    from routes import category_routes
    app.register_blueprint(category_routes.bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True) 