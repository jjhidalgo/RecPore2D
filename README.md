# RecPor2D
Creates rectangular 2D porous media with regular or random packing of discs.
The geometry can be written in GMSH, OpenSCAD and SnappyHexMesh (OpenFOAM) format.

RecPore2D.py: Module to create 2D porous media with regular or ramdon packing of discs.

PoreError.py: Manages exceptions raised by RecPore2D.

PyGmsh.py: gmsh wrapper.

PyGrain.py: Manages the creation and properties of discs (grains).

PyOpenSCAD.py: OpenSCAD wrapper.

PySnappy.py: SnappyHexMesh wrapper.

blockMeshDict.tmpl: Template for blockMesh dictionary.

snappy.tmpl: Template for SnappyHexMesh dictionary.

test.py : A test for regular porous media.

test-rnd.py: A test for random porous media.

testsnappy.py: A test for SnappyHexMesh generation.

Acknowledgements:

Project MHetScale (FP7-IDEAS-ERC-617511) European Research Council

Project Mec-MAT (CGL2016-80022-R) Spanish Ministry of Economy and Competitiveness
