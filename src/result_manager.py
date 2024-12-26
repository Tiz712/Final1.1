import json
import os
import networkx as nx
from datetime import datetime
from typing import Dict, List

class ResultManager:
    def __init__(self, storage_dir: str = "results"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
    def save_result(self, problem_data: Dict, reasoning_graph: nx.Graph) -> str:
        """Save reasoning results and graph"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_id = f"result_{timestamp}"
        
        # Convert graph to serializable format
        graph_data = {
            "nodes": [[n, attr] for n, attr in reasoning_graph.nodes(data=True)],
            "edges": list(reasoning_graph.edges(data=True))
        }
        
        # Combine all data
        result_data = {
            "id": result_id,
            "timestamp": timestamp,
            "problem": problem_data,
            "graph": graph_data
        }
        
        # Save to JSON file
        filepath = os.path.join(self.storage_dir, f"{result_id}.json")
        with open(filepath, "w") as f:
            json.dump(result_data, f, indent=2)
            
        return result_id
    
    def load_result(self, result_id: str) -> Tuple[Dict, nx.Graph]:
        """Load saved result and reconstruct graph"""
        filepath = os.path.join(self.storage_dir, f"{result_id}.json")
        
        with open(filepath, "r") as f:
            data = json.load(f)
            
        # Reconstruct graph
        graph = nx.Graph()
        for node, attr in data["graph"]["nodes"]:
            graph.add_node(node, **attr)
        for u, v, attr in data["graph"]["edges"]:
            graph.add_edge(u, v, **attr)
            
        return data["problem"], graph
        
    def list_results(self) -> List[str]:
        """List all saved results"""
        return [f.replace(".json", "") for f in os.listdir(self.storage_dir) 
                if f.endswith(".json")]