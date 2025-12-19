
import gmsh

gmsh.initialize()
gmsh.open("snappyHexMeshDict.geo")
gmsh.model.mesh.generate(3)  # 3D
gmsh.fltk.run()
gmsh.finalize()
