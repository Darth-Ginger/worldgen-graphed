from apiflask import APIFlask
from flask import request, jsonify
from neo4j import GraphDatabase
import os

app = APIFlask(__name__)

# Neo4j configuration
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')

neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
