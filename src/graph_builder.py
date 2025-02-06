import networkx as nx

def build_graph(page_data):
    """
    Build a NetworkX directed graph from a list of page details.
    Each page becomes a node with its categories.
    Each link from one page to another becomes an edge.
    """
    G = nx.DiGraph()
    # First, create a set of all page titles we've fetched
    fetched_pages = {page["title"] for page in page_data}

    for page in page_data:
        title = page["title"]
        categories = page["categories"]
        links = page["links"]
        G.add_node(title, categories=categories)
        for link in links:
            # Only create edge if the target page is in our fetched set
            if link in fetched_pages:
                G.add_edge(title, link)
    return G

def get_graph_data(G):
    """
    Convert the NetworkX graph into a dictionary containing nodes and edges.
    This structure is ready to be serialized as JSON.
    """
    data = {
        "nodes": [],
        "edges": []
    }
    for node, attrs in G.nodes(data=True):
        data["nodes"].append({
            "id": node,
            "categories": attrs.get("categories", [])
        })
    for source, target in G.edges():
        data["edges"].append({
            "source": source,
            "target": target
        })
    return data 