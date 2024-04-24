from neo4j import GraphDatabase
import json

# Neo4j connection settings
with open("../config.json") as config_file:
    config = json.load(config_file)

uri = config.get("NEO4J_URI")
username = config.get("NEO4J_USERNAME")
password = config.get("NEO4J_PASSWORD")

# Function to retrieve data from Neo4j and write to a text file
def retrieve_data_and_write(file_path, graph_id):
    # Connect to the Neo4j database
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        # Cypher query to retrieve data
        cypher_query = (
            "MATCH (e1)-[r]->(e2) "
            "WHERE e1.graph_id = $graph_id AND e2.graph_id = $graph_id AND r.graph_id = $graph_id "
            "RETURN e1.name AS entity1, type(r) AS relation, e2.name AS entity2"
        )
        result = session.run(cypher_query, graph_id=graph_id)

        # Write data to a text file
        with open(file_path, 'w') as file:
            for record in result:
                line = f"[{record['entity1']}]-({record['relation']})->[{record['entity2']}]\n"
                file.write(line)

    # Close the Neo4j driver
    driver.close()

# Path to save the generated data file
output_file_path = "output_rela_file.txt"

# Retrieve data from Neo4j and write to a file
retrieve_data_and_write(output_file_path, "graph1")
