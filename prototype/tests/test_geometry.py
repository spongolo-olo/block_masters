import pytest
from core.geometry import TruncatedOctahedron

def test_truncated_octahedron_vertex_count():
    to = TruncatedOctahedron()
    assert to.vertex_count == 24

def test_truncated_octahedron_face_count():
    to = TruncatedOctahedron()
    assert to.face_count == 14

def test_truncated_octahedron_edge_count():
    to = TruncatedOctahedron()
    assert to.edge_count == 36

def test_truncated_octahedron_vertices_presence():
    to = TruncatedOctahedron()
    assert (0, 1, 2) in to.vertices
    assert (0, -1, -2) in to.vertices
