from dotenv import load_dotenv
import os
from langchain_community.graphs import Neo4jGraph
import warnings

warnings.filterwarnings("ignore")
load_dotenv('.env', override=True)


NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



graph = Neo4jGraph(
    url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
)

print(graph.schema)

validation_query = """
MATCH (lc:Learning_Concept)
RETURN lc.name AS Learning_Concept
"""
existing_concepts = graph.query(validation_query)
print(existing_concepts)