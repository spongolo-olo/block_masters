import pytest
from core.lattice import Lattice

def test_lattice_initialization_is_empty():
    lattice = Lattice()
    assert len(lattice.get_blocks()) == 0

def test_place_root_block():
    lattice = Lattice()
    lattice.place_block((0, 0, 0), color="red")
    assert len(lattice.get_blocks()) == 1
    assert lattice.get_block((0, 0, 0)) == {"color": "red"}

def test_invalid_lattice_coordinates():
    lattice = Lattice()
    # Coordinates must satisfy u = v = w (mod 2)
    with pytest.raises(ValueError):
        lattice.place_block((1, 0, 0)) # 1 is odd, 0 is even -> Invalid!

def test_get_neighbors_info():
    lattice = Lattice()
    lattice.place_block((0, 0, 0))
    neighbors = lattice.get_face_neighbors((0, 0, 0))
    
    assert len(neighbors) == 14
    # Check square face neighbor offsets (scaled by 1 in BCC indices, i.e., offsets of +/-2 on one axis)
    assert ((2, 0, 0), "square") in [(n["coord"], n["type"]) for n in neighbors]
    assert ((-2, 0, 0), "square") in [(n["coord"], n["type"]) for n in neighbors]
    
    # Check hexagon face neighbor offsets (offsets of +/-1 on all axes)
    assert ((1, 1, 1), "hexagon") in [(n["coord"], n["type"]) for n in neighbors]
    assert ((-1, -1, -1), "hexagon") in [(n["coord"], n["type"]) for n in neighbors]

def test_click_to_place_block_on_face():
    lattice = Lattice()
    lattice.place_block((0, 0, 0), color="red")
    
    # Place a block on the hexagon face (1, 1, 1)
    lattice.place_on_face((0, 0, 0), face_direction=(1, 1, 1), color="blue")
    
    # The new block should be at (1, 1, 1) in BCC coordinates
    assert lattice.get_block((1, 1, 1)) == {"color": "blue"}
    assert len(lattice.get_blocks()) == 2
