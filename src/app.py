import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from geometric_reasoner import GeometricReasoner
from llm_interface import LLMInterface
from result_manager import ResultManager
import os

class GeometricReasoningApp:
    def __init__(self):
        self.reasoner = GeometricReasoner()
        self.graph = nx.Graph()
        self.result_manager = ResultManager()
        
        # Initialize LLM interface with API key
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = LLMInterface(api_key)
        else:
            st.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
            self.llm = None
        
    def run(self):
        st.title("Geometric Reasoning System")
        
        # Problem input
        st.header("Problem Description")
        description = st.text_area("Enter the geometric problem:")
        
        if st.button("Analyze Problem") and self.llm:
            analysis = self.llm.analyze_problem(description)
            st.write("Problem Analysis:", analysis)
            
            # Create graph from analysis
            self.create_graph_from_analysis(analysis)
            
            # Save results
            result_id = self.result_manager.save_result(
                {"description": description, "analysis": analysis},
                self.graph
            )
            st.success(f"Results saved with ID: {result_id}")
        
        # Load previous results
        st.sidebar.header("Previous Results")
        results = self.result_manager.list_results()
        selected_result = st.sidebar.selectbox("Load previous result", [""] + results)
        
        if selected_result:
            problem_data, graph = self.result_manager.load_result(selected_result)
            self.graph = graph
            st.sidebar.write("Problem:", problem_data["description"])
        
        # Original controls
        with st.sidebar:
            st.header("Manual Controls")
            
            # Add point
            st.subheader("Add Point")
            x = st.number_input("X coordinate", value=0.0)
            y = st.number_input("Y coordinate", value=0.0)
            if st.button("Add Point"):
                self.add_point(x, y)
            
            # Add line
            st.subheader("Add Line")
            points = list(self.graph.nodes())
            if len(points) >= 2:
                p1 = st.selectbox("Point 1", points)
                p2 = st.selectbox("Point 2", points)
                if st.button("Add Line"):
                    self.add_line(p1, p2)
        
        # Display area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.display_graph()
            
        with col2:
            st.subheader("Verification")
            if st.button("Verify Construction"):
                self.verify_construction()
    
    def create_graph_from_analysis(self, analysis):
        """Create graph from LLM analysis"""
        # Clear existing graph
        self.graph.clear()
        
        # Add entities as nodes
        if "entities" in analysis:
            for entity in analysis["entities"]:
                self.graph.add_node(entity["name"], **entity.get("properties", {}))
        
        # Add relationships as edges
        if "relationships" in analysis:
            for rel in analysis["relationships"]:
                self.graph.add_edge(rel["from"], rel["to"], 
                                  type=rel.get("type", "unknown"))
    
    # ... (rest of the methods remain the same)