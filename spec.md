# Block Masters: Technical Specification

## 1. Project Overview
**Block Masters** is a 3D procedural world-generation project. Unlike traditional voxel engines that utilize cubes (Axis-Aligned Bounding Boxes), Block Masters utilizes the **truncated octahedron** as its fundamental volumetric unit. The goal is to create a visually unique, mathematically elegant, and computationally fascinating space-filling environment.

## 2. Core Geometry: The Truncated Octahedron
The fundamental building block is an Archimedeed solid with the following properties:
- **Faces:** 14 (8 regular hexagons, 6 squares).
- **Vertices:** 24.
- **Edges:** 36.
- **Space-Filling Property:** The shape is a space-filling polyhedron, specifically forming the **bitruncated cubic honeycomb** tessellation. This allows for gapless, non-overlapping 3D world construction.

## 3. Technology Stack & Prototyping
- **Prototyping Languages:** Python or JavaScript (to allow for rapid iteration and high-level logic testing).
- **Final Implementation Target:** **Rust** (for high-performance, memory-safe execution of complex geometry and physics).
- **Deployment/Testing Platform:** Web-based prototype accessible via a web browser (utilizing **WebGL** or **WebGPU**) hosted on a VPS.
- **Development Methodology:** **Red-Green-Refactor (TDD)**. All core geometric and placement logic must be verified via unit tests before implementation in the rendering layer.

##  4. Gameplay Mechanics
- **Initial Phase:** Simple, visually distinct colored blocks.
- **Placement Engine:** Players can place a new block by clicking an existing face of a block in the lattice. The new block will "snap" to the adjacent position in the bitruncated cubic honeycomb.
- **Future Scope:** Introduction of complex block behaviors, interactive properties, and advanced environmental interactions.

## 5. Technical Domains & Requirements

### A. Geometry & Tessellation Engine
- **Vertex Generation:** Algorithms to generate the precise coordinates of a truncated octahedron based on a lattice position.
- **Adjacency Logic:** Implementation of the connectivity rules for the bitruncated cubic honeycomb (identifying which faces meet which neighbors).
- **Prototyping:** Verification of the geometric integrity using Python-based mathematical proofs.

### B. Rendering Pipeline (Mesh Generation & WebGL)
- **Manifold Mesh Construction:** A system to generate a single, continuous, manifold triangular mesh from a collection of polyhedra.
- **Web-Based Rendering:** Utilizing **Three.js** (or similar) for the prototype to enable browser-based interaction.
- **Face Culling & Optimization:** Efficiently removing internal faces (faces shared by two blocks) to minimize polygon count and improve GPU performance.

### C. Collision & Physics
- **Non-AABB Collision:** Implementation of the **GJK (Gilbert-Johnson-Keerthi)** algorithm for collision detection between arbitrary convex polyhedra.
- **EPA (Expanding Polytope Algorithm):** For calculating penetration depth and contact normals during collisions.

### D. Data Structures & World Management
- **Spatial Partitioning:** Developing a data structure (e.g., an Octree or a specialized Polyhedral Grid) capable of efficiently storing and querying truncated octahedra in a 3D volume.
- **Procedural Generation:** Implementing noise functions (Perlin/Simplex) to determine block density and terrain height within the space-filling lattice.

## 6. Development Roadmap
- **Phase 0: Prototyping Environment & TDD Setup.** Establishing the Python/JS testing framework and the web-based rendering loop.
- **Phase 1: Mathematical Foundation.** Python-based verification of geometry and tessellation.
- **Phase 2: The Single Cell & Web Rendering.** 3/D rendering of a single, textured, interactive truncated octahedron in the browser.
- **Phase 3: The Lattice & Placement Logic.** Implementation of the mesh generation algorithm and the "click-to-place" logic (Red-Green-Refactor).
- **Phase 4: The Rust Transition.** Porting the core, high-performance math and engine logic to Rust for production-grade performance.

---
**Status:** Initialized (Updated with Web-Prototype & TDD requirements).
**Agent:** Spongolo (Execution Agent)
**Architect:** Mallard (Philip)
