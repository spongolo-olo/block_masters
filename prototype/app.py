from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import os
from core.geometry import TruncatedOctahedron
from core.lattice import Lattice

app = Flask(__name__, static_folder='/workspace/block_masters/prototype/web')
CORS(app) # Enable CORS for easy cross-origin testing

# Initialize Engines
geometry_engine = TruncatedOctahedron()
lattice_engine = Lattice()

# Place a default root block at (0, 0, 0)
lattice_engine.place_block((0, 0, 0), color="red")

@app.route('/')
def index():
    return send_from_directory('/workspace/block_masters/prototype/web', 'index.html')

@app.route('/api/geometry')
def get_geometry():
    """Returns the geometry of a single truncated octahedron as JSON."""
    return jsonify({
        "vertices": geometry_engine.vertices,
        "faces": geometry_engine.faces,
        "edges": geometry_engine.edges,
        "vertex_count": geometry_engine.vertex_count,
        "face_count": geometry_engine.face_count,
        "edge_count": geometry_engine.edge_count
    })

@app.route('/api/lattice', methods=['GET'])
def get_lattice():
    """Returns all blocks in the lattice with their centers."""
    blocks_data = []
    for coord, block in lattice_engine.get_blocks().items():
        u, v, w = coord
        # The physical center is 2 * (u, v, w)
        center = (2 * u, 2 * v, 2 * w)
        blocks_data.append({
            "coord": list(coord),
            "center": list(center),
            "color": block.get("color", "green")
        })
    return jsonify(blocks_data)

@app.route('/api/lattice/place', methods=['POST'])
def place_block():
    """Places a new block relative to an existing one."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400
        
    coord = data.get("coord")
    face_direction = data.get("face_direction")
    color = data.get("color", "green")
    
    if not coord or not face_direction:
        return jsonify({"error": "coord and face_direction are required parameters"}), 400
        
    try:
        # Convert list inputs to tuples
        coord_tuple = tuple(coord)
        direction_tuple = tuple(face_direction)
        
        lattice_engine.place_on_face(coord_tuple, direction_tuple, color=color)
        
        # Return the updated lattice
        return get_lattice()
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/lattice/reset', methods=['POST'])
def reset_lattice():
    """Resets the lattice to just the single root block for testing."""
    global lattice_engine
    lattice_engine = Lattice()
    lattice_engine.place_block((0, 0, 0), color="red")
    return get_lattice()

# Prevent caching of all assets to ensure mobile browsers immediately receive fresh code
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)