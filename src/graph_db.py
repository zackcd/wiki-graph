from neo4j import GraphDatabase

class GraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def create_node(self, title, categories):
        with self.driver.session() as session:
            session.write_transaction(self._create_node_tx, title, categories)
    
    @staticmethod
    def _create_node_tx(tx, title, categories):
        query = (
            "MERGE (p:Page {title: $title}) "
            "SET p.categories = $categories "
            "RETURN p"
        )
        tx.run(query, title=title, categories=categories)
    
    def create_edge(self, source, target):
        with self.driver.session() as session:
            session.write_transaction(self._create_edge_tx, source, target)
    
    @staticmethod
    def _create_edge_tx(tx, source, target):
        query = (
            "MATCH (a:Page {title: $source}) "
            "MERGE (b:Page {title: $target}) "
            "MERGE (a)-[:LINKS_TO]->(b)"
        )
        tx.run(query, source=source, target=target)
    
    def load_graph(self, graph):
        # Iterate over the NetworkX graph to load nodes and edges into Neo4j
        for node, attrs in graph.nodes(data=True):
            self.create_node(node, attrs.get("categories", []))
        for source, target in graph.edges():
            self.create_edge(source, target) 