from neo4j import GraphDatabase
import json

# Neo4j connection settings
with open("../config.json") as config_file:
    config = json.load(config_file)

uri = config.get("NEO4J_URI")
username = config.get("NEO4J_USERNAME")
password = config.get("NEO4J_PASSWORD")

# Function to read data from file and upload to Neo4j
def upload_data(file_path, graph_id):
    # Connect to the Neo4j database
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming format: [Entity1]-(relation)->[Entity2]
                data = line.strip().split("-")
                entity1 = data[0][1:-1]
                relation = data[1][1:-1]
                entity2 = data[2][2:-1]

                #print(entity1)
                #print(relation)
                #print(entity2)
                # Create nodes and relationship in Neo4j
                cypher_query = (
                    f"MERGE (e1:Entity {{name: $entity1, graph_id: $graph_id}}) "
                    f"MERGE (e2:Entity {{name: $entity2, graph_id: $graph_id}}) "
                    f"MERGE (e1)-[:{relation} {{graph_id: $graph_id}}]->(e2)"
                )
                session.run(cypher_query, entity1=entity1, entity2=entity2, graph_id=graph_id)

    # Close the Neo4j driver
    driver.close()

# Path to your data file
file_path = "sample_data2.txt"

# Upload data to Neo4j
upload_data(file_path, "graph1")