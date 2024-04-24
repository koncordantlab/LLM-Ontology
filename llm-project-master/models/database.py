from neo4j import GraphDatabase
import json

def get_keys():
    # Neo4j connection settings
    with open("config.json") as config_file:
        config = json.load(config_file)

    uri = config.get("NEO4J_URI")
    username = config.get("NEO4J_USERNAME")
    password = config.get("NEO4J_PASSWORD")
    return uri, username, password

def upload_data(file_path, graph_id):
    print("here0")
    uri, username, password = get_keys()
    print("here1")
    # Connect to the Neo4j database
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        with open(file_path, 'r') as file:
            for line in file:
                # Assuming format: [Entity1]-(relation)-[Entity2]
                if line == "" or line is None:
                    continue
                if "-" not in line:
                    continue
                data = line.strip().split("-")
                entity1 = data[0]
                relation = data[1]
                entity2 = data[2]

                print(entity1)
                print(relation)
                print(entity2)
                # Create nodes and relationship in Neo4j
                cypher_query = (
                    f"MERGE (e1:Entity {{name: $entity1, graph_id: $graph_id}}) "
                    f"MERGE (e2:Entity {{name: $entity2, graph_id: $graph_id}}) "
                    f"MERGE (e1)-[:{relation} {{graph_id: $graph_id}}]->(e2)"
                )
                session.run(cypher_query, entity1=entity1, entity2=entity2, graph_id=graph_id)

    # Close the Neo4j driver
    driver.close()


def retrieve_data_and_write(file_path, graph_id):
    uri, username, password = get_keys()

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
                line = f"{record['entity1']}-{record['relation']}-{record['entity2']}\n"
                file.write(line)

    # Close the Neo4j driver
    driver.close()

def get_all_graph_ids():
    uri, username, password = get_keys()
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        cypher_query = (
            "MATCH (n) "
            "WITH DISTINCT n.graph_id AS graph_id "
            "RETURN COLLECT(graph_id) AS graph_ids"
        )
        result = session.run(cypher_query)
        graph_ids = result.single()["graph_ids"]
    driver.close()
    return graph_ids