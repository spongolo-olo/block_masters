class Lattice:
    """
    Manages the 3D space-filling lattice of truncated octahedrons
    using a body-centered cubic (BCC) coordinate system.
    
    Coordinates are stored as (u, v, w) where:
    - u, v, w are integers
    - u ≡ v ≡ w (mod 2)
    
    The physical center of a block is at (2*u, 2*v, 2*w).
    """
    def __init__(self):
        self.blocks = {}

    def _validate_coordinates(self, coord: tuple):
        if not isinstance(coord, tuple) or len(coord) != 3:
            raise ValueError("Coordinates must be a 3-tuple.")
        
        u, v, w = coord
        # Verify that all are integers
        if not all(isinstance(x, int) for x in [u, v, w]):
            raise ValueError("Lattice coordinates must be integers.")
            
        # Verify u ≡ v ≡ w (mod 2)
        if (u % 2) != (v % 2) or (v % 2) != (w % 2):
            raise ValueError("Invalid BCC coordinate: u, v, w must have the same parity.")

    def place_block(self, coord: tuple, color: str = "green"):
        self._validate_coordinates(coord)
        self.blocks[coord] = {"color": color}

    def get_block(self, coord: tuple):
        self._validate_coordinates(coord)
        return self.blocks.get(coord)

    def get_blocks(self) -> dict:
        return self.blocks

    def get_face_neighbors(self, coord: tuple) -> list:
        self._validate_coordinates(coord)
        u, v, w = coord
        neighbors = []

        # 1. 6 Square Face offsets
        square_offsets = [
            (2, 0, 0), (-2, 0, 0),
            (0, 2, 0), (0, -2, 0),
            (0, 0, 2), (0, 0, -2)
        ]
        for du, dv, dw in square_offsets:
            target = (u + du, v + dv, w + dw)
            neighbors.append({
                "coord": target,
                "type": "square",
                "offset": (du, dv, dw),
                "occupied": target in self.blocks
            })

        # 2. 8 Hexagon Face offsets
        hexagon_offsets = [
            (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
            (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)
        ]
        for du, dv, dw in hexagon_offsets:
            target = (u + du, v + dv, w + dw)
            neighbors.append({
                "coord": target,
                "type": "hexagon",
                "offset": (du, dv, dw),
                "occupied": target in self.blocks
            })

        return neighbors

    def place_on_face(self, coord: tuple, face_direction: tuple, color: str = "green"):
        self._validate_coordinates(coord)
        self._validate_coordinates(face_direction)
        
        # Verify that face_direction is a valid offset
        abs_offset = tuple(abs(x) for x in face_direction)
        is_square = abs_offset in [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
        is_hexagon = abs_offset == (1, 1, 1)
        
        if not (is_square or is_hexagon):
            raise ValueError("face_direction must be a valid face offset.")
            
        u, v, w = coord
        du, dv, dw = face_direction
        target = (u + du, v + dv, w + dw)
        
        if target in self.blocks:
            raise ValueError(f"Lattice position {target} is already occupied.")
            
        self.place_block(target, color=color)
