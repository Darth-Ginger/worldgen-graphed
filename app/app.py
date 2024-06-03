from apiflask import APIFlask
from flask import request, jsonify
from neo4j import GraphDatabase
import os
from config import Config


conf = Config()
app = APIFlask(__name__)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
