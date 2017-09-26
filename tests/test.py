# Test for RegPore2D.

from RecPore2D import RegPore2D as rg
a = rg(nx=23,ny=23,radius=0.02,packing='tri')
b = rg(nx=11,ny=11,radius=0.04,packing='tri')

b.xoffset = 3.3
a.size = 0.8*a.throat
b.size = 0.8*b.throat

c = a + b

#a.set_bounding_box([0.0,0.0,0.5], [1.0,1.0,1.0])

a.write_mesh(fname='a.geo', meshtype='gmsh')
#a.write_mesh(meshtype='snappy')
#b.write_mesh(fname='b.geo', meshtype='gmsh')
c.write_mesh(fname='c.geo', meshtype='gmsh')
#c.write_mesh(fname='c.scad', meshtype='oscad')
#c.write_mesh(meshtype='snappy')
c.is3D=True
c.write_mesh(fname='c.stl',meshtype='stl')


