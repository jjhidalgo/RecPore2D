# Test for RegPore2D 3D option.

from RecPore2D import RndPore2D as rndp
a = rndp(lx=1., ly=1., rmin=0.01, rmax=0.01, target_porosity=0.4, packing='rnd')
a.size = 0.001
a.is3D = True
rmax = 0.01
pmin = [0.0, 0.0, 0.5-rmax]
pmax = [1.0, 1.0, 0.5+rmax]
a.bounding_box = [pmin, pmax]

a.write_mesh(meshtype='snappy')
a.write_mesh(fname='rnd3D.geo', meshtype='gmsh')
a.write_mesh(fname='rnd3D.stl', meshtype='stl')


 
