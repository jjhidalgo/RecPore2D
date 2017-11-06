# Test for RegPore2D.

from RecPore2D import RegPore2D as rp
a = rp(nx=11,ny=5,radius=0.02,packing='tri')


#a.bounding_box=[[0.0,0.0,0.5], [1.0,1.0,1.0]]
a.write_mesh(meshtype='snappy')
a.write_mesh(fname='a.geo',meshtype='gmsh')


