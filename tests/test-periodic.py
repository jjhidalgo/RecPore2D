# Test for RecPore2D.

from RecPore2D import RegPore2D as rg
a = rg(nx=4,ny=4, packing='tri')
a.isPeriodic = False
a.ly = 1.0
a.size = 0.8*a.throat
a.write_mesh(fname='a.geo', meshtype='gmsh')

b = rg(nx=4,ny=4, packing='tri')
b.isPeriodic = True
b.ly = 1.0
b.size = 0.8*a.throat
b.write_mesh(fname='b.geo', meshtype='gmsh')

