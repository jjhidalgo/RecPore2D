# Test for RecPore2D.

from RecPore2D import RndPore2D as rndp
a = rndp(lx=0.02, ly=0.01, rmin=0.00025, rmax=0.00055, target_porosity=0.57, packing='rnd')
a.size = 0.00001
pmin = [0.0, 0.0, 0.0]
pmax = [0.02, 0.01, 0.000000002]
a.bounding_box = [pmin, pmax]

#a.write_mesh(fname='snappyHexMeshDict.geo', meshtype='gmsh')
#a.write_mesh(fname='snappyHexMeshDict', meshtype='stl')
a.write_mesh(fname='snappyHexMeshDict', meshtype='snappy')


