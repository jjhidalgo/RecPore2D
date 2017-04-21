# Test for RegPore2D 3D option.

from RecPore2D import RndPore2D as rndp
a = rndp(lx=1., ly=1., rmin=0.01, rmax=0.01, target_porosity=0.4, packing='rnd')
a.size = 0.001
a.is3D = True
pmin = [0.0, 0.0, 0.499]
pmax = [1.0, 1.0, 0.501]
a.bounding_box = [pmin, pmax]

a.write_mesh(meshtype='snappy')
a.write_mesh(fname='rnd3D.geo', meshtype='gmsh')


