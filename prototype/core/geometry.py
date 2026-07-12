import itertools
import math

class TruncatedOctahedron:
    """
    Represents a Truncated Octahedron, an Archimedean solid.
    Vertices are all permutations of (0, +/- 1, +/- 2).
    """
    def __init__(self):
        self.vertices = self._generate_vertices()
        self.faces = self._generate_faces()
        self.edges = self._generate_edges()

    def _generate_vertices(self) -> list:
        vertices = []
        # All permutations of (0, 1, 2)
        for p in itertools.permutations([0, 1, 2]):
            # All combinations of signs for the non-zero elements
            for signs in itertools.product([1, -1], repeat=2):
                v = list(p)
                # Apply signs to the non-zero elements
                sign_idx = 0
                for i in range(3):
                    if v[i] != 0:
                        v[i] *= signs[sign_idx]
                        sign_idx += 1
                vertices.append(tuple(v))
        return list(set(vertices))

    def _generate_faces(self) -> list:
        faces = []
        
        # 1. Square Faces (6)
        # Planes: x = +/- 2, y = +/- 2, z = +/- 2
        for axis in range(3):
            for sign in [1, -1]:
                face_v_indices = []
                for idx, v in enumerate(self.vertices):
                    if v[axis] == 2 * sign:
                        face_v_indices.append(idx)
                
                if len(face_v_indices) == 4:
                    # Use the center of the face to find the order
                    center = self._get_face_center(face_v_indices)
                    ordered = self._order_vertices_on_plane(face_v_indices, center)
                    if ordered:
                        faces.append(ordered)

        # 2. Hexagon Faces (8)
        # Planes: sx*x + sy*y + sz*z = 3 where sx, sy, sz in {1, -1}
        for sx, sy, sz in itertools.product([1, -1], repeat=3):
            face_v_indices = []
            for idx, v in enumerate(self.vertices):
                if sx * v[0] + sy *v[1] + sz * v[2] == 3:
                    face_v_indices.append(idx)
                
            if len(face_v_indices) == 6:
                center = self._get_face_center(face_v_indices)
                ordered = self._order_vertices_on_plane(face_v_indices, center)
                if ordered:
                    faces.append(ordered)

        return faces

    def _get_face_center(self, vertex_indices: list) -> tuple:
        center = [0.0, 0.0, 0.0]
        for idx in vertex_indices:
            for i in range(3):
                center[i] += self.vertices[idx][i]
        for i in range(3):
            center[i] /= len(vertex_indices)
        return tuple(center)

    def _order_vertices_on_plane(self, vertex_indices: list, center: tuple) -> list:
        if not vertex_indices:
            return []
        
        # 1. Face Normal (from origin to center)
        normal = center
        mag = math.sqrt(sum(c**2 for c in normal))
        if mag == 0: return vertex_indices
        normal = tuple(c/mag for c in normal)

        # 2. Define 2D coordinate system (u, v)
        # Pick an arbitrary vector 'w' not parallel to 'normal'
        w = (1, 0, 0) if abs(normal[0]) < 0.9 else (0, 1, 0)
        
        # u = normal x w
        u = (
            normal[1] * w[2] - normal[2] * w[1],
            normal[2] * w[0] - normal[0] * w[2],
            normal[0] * w[1] - normal[1] * w[0]
        )
        mag_u = math.sqrt(sum(c** 2 for c in u))
        u = tuple(c/mag_u for c in u)

        # v = normal x u
        v = (
            normal[1] * u[2] - normal[2] * u[1],
            normal[2] * u[0] - normal[0] * u[2],
            normal[0] * u[1] - normal[1] * u[0]
        )

        # 3. Project each vertex and sort by angle
        projected_points = []
        for idx in vertex_indices:
            p = self.vertices[idx]
            # Vector from center to point
            rel_p = (p[0]-center[0], p[1]-center[1], p[2]-center[2])
            # 2D coordinates in (u, v) basis
            x_2d = sum(rel_p[i] * u[i] for i in range(3))
            y_2d = sum(rel_p[i] * v[i] for i in range(3))
            projected_points.append((math.atan2(y_2d, x_2d), idx))

        projected_points.sort()
        return [p[1] for p in projected_points]

    def _generate_edges(self) -> list:
        edges = set()
        for face in self.faces:
            for i in range(len(face)):
                v1 = face[i]
                v2 = face[(i + 1) % len(face)]
                edges.add(tuple(sorted((v1, v2))))
        return list(edges)

    @property
    def vertex_count(self) -> int:
        return len(self.vertices)

    @property
    def face_count(self) -> int:
        return len(self.faces)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

if __name__ == "__main__":
    to = TruncatedOctahedron()
    print(f"Vertices: {to.vertex_count}")
    print(f"Faces: {to.face_count}")
    print(f"Edges: {to.edge_count}")
