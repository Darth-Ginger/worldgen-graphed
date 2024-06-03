from arango import ArangoClient
from arango.database import StandardDatabase
import os
from typing import Dict, Any, List, Optional
from config import Config


class ArangoDBDriver:
    sys_db = None
    db = None
    
    def __init__(
        self, 
        config: Dict[str, Any] = Config.db_config, 
        initialize: bool = False,
        **kwargs: Dict[str, Any]
        ):
        
        self.host     = config['DB_HOST']
        self.port     = config['DB_PORT']
        self.db_name  = config['DB_NAME']
        self.username = config['DB_USER']
        self.password = config['DB_PASS']
        self.sys_user = config['SYS_DB_USER']
        self.sys_pass = config['SYS_DB_PASS']

        client = ArangoClient(hosts=f"http://{self.host}:{self.port}")
        self.sys_db: StandardDatabase  = client.db('_system', username=self.sys_user, password=self.sys_pass)

        if not self.sys_db.has_database(self.db_name) and initialize:
            self.sys_db.create_database(self.db_name)
            self.sys_db.update_permission(username=self.username, permission='rw', database=self.db_name)
        
        try:
            self.db: StandardDatabase = client.db(self.db_name, username=self.username, password=self.password)
        except Exception as e:
            print(e)

#region dunders
    def __enter__(self) -> 'ArangoDBDriver':
        if self.sys_db is None or self.db is None:
            raise RuntimeError("ArangoDBDriver instance is not initialized")
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sys_db = None
        self.db = None

#endregion dunders

#region CRUD basics
    def create_node(self, collection_name: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        collection = self.db.collection(collection_name)
        meta = collection.insert(properties)
        return collection.get(meta['_key'])

    def delete_node(self, collection_name: str, node_key: str) -> bool:
        collection = self.db.collection(collection_name)
        collection.delete(node_key)
        return not collection.has(node_key)

    def update_node(self, collection_name: str, node_key: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        collection = self.db.collection(collection_name)
        collection.update_match({'_key': node_key}, properties)
        return collection.get(node_key)

    def get_node_properties(self, collection_name: str, filters: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        collection = self.db.collection(collection_name)
        cursor = collection.find(filters)
        result = cursor.next()
        return result if result else None

#endregion CRUD basics

#region Utility Functions

    def node_exists(self, collection_name: str, filters: Dict[str, Any]) -> bool:
        collection = self.db.collection(collection_name)
        cursor = collection.find(filters)
        return cursor.count() > 0

#endregion Utility Functions

#region Example usage
if __name__ == "__main__":
    conf = {
        "DB_HOST": "10.20.0.40", 
        "DB_PORT":"8529", 
        "DB_NAME": "worldgen",
        "DB_USER": "worldgen", 
        "DB_PASS": "worldgen", 
        "SYS_DB_USER": 'root', 
        "SYS_DB_PASS": 'kweRJ9D6iN2'
    }
    
    with ArangoDBDriver(conf) as driver:
        node_properties = {"name": "Alice", "age": 30}
        created_node = driver.create_node("nodes", node_properties)
        print(f"Created node: {created_node}")

        node_properties = driver.get_node_properties("nodes", {"name": "Alice"})
        print(f"Node properties: {node_properties}")

        node_exists = driver.node_exists("nodes", {"name": "Alice"})
        print(f"Node exists: {node_exists}")

        updated_node = driver.update_node("nodes", created_node["_key"], {"age": 31})
        print(f"Updated node: {updated_node}")

        # deleted = driver.delete_node("nodes", created_node["_key"])
        # print(f"Deleted: {deleted}")
        
#endregion Example usage