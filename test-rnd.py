# Test for RegPore2D.

from RecPore2D import RndPore2D as rndp
a = rndp(lx=1., ly=1., rmin=0.01, rmax=0.05, target_porosity=0.4, packing='rnd')
a.size = 0.001
pmin = [0.0, 0.0, 0.5]
pmax = [1.0, 1.0, 1.5]
a.bounding_box = [pmin, pmax]

a.write_mesh(fname='rnd.geo', meshtype='gmsh')


