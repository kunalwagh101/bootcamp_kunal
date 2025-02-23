"""
No.12 Serializing Cyclic References: Handle serialization of objects with cyclic references.
Create a scenario where two objects reference each other and implement a way to serialize and deserialize them correctly
"""

import json

class Node:
    def __init__(self, name):
        self.name = name
        self.partner = None

    def __repr__(self):
        partner_name = self.partner.name if self.partner else None
        return f"Node({self.name}, partner={partner_name})"

def serialize(node, visited=None):
   
    if visited is None:
        visited = {}
    if id(node) in visited:
        return {"__ref__": visited[id(node)]}
    
 
    node_id = f"node_{len(visited)+1}"
    visited[id(node)] = node_id
   
    return {
        "__id__": node_id,
        "name": node.name,
        "partner": serialize(node.partner, visited) if node.partner else None
    }

def deserialize(data, nodes=None):

    if nodes is None:
        nodes = {}
    if "__ref__" in data:
        return nodes[data["__ref__"]]
    
    node_id = data["__id__"]
    node = Node(data["name"])
    nodes[node_id] = node
    
   
    if data["partner"]:
        node.partner = deserialize(data["partner"], nodes)
    return node

if __name__ == "__main__":
        
    
    obj_1 = Node("obj_1")
    obj_2 = Node("obj_2")
    obj_1.partner = obj_2
    obj_2.partner = obj_1

    print("Original objects:")
    print("obj_1:", obj_1)
    print("obj_2:", obj_2)

    serialized = serialize(obj_1)
    json_str = json.dumps(serialized, indent=2)
    print("\nSerialized JSON:")
    print(json_str)

    loaded = json.loads(json_str)
    new_obj_1 = deserialize(loaded)
    print("\nDeserialized objects:")
    print("new_obj_1:", new_obj_1)
    print("new_obj_1.partner:", new_obj_1.partner)
    print("Cyclic check:", new_obj_1.partner.partner is new_obj_1)