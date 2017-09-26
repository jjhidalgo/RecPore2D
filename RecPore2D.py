"""2D rectangular porous medium generation"""

import warnings
import numpy as np
import PoreError as PoreError

class RecPore2D(object):
    """Rectangular porous medium."""

    def __init__(self):

        self._packing = None
        self._ngrains = None
        self._circles = None
        self._xoffset = 0.0
        self._bbox_pmin = None
        self._bbox_pmax = None
        self._bbox_set = False
        self._nblocks = [200, 200, 200]
        self._lx = None
        self._ly = None
        self._size = None
        self._is3D = False
        self._zeta = 0.5
        self._packing_done = False
        self._circles_done = False

#
#-----------------------------------------------------------------------
#
    @property
    def packing(self):
        """Gets packing."""

        return self._packing
#
#-----------------------------------------------------------------------
#
    @packing.setter
    def packing(self, value):
        """Defined by children."""

        pass
#
#-----------------------------------------------------------------------
#
    @property
    def ngrains(self):
        """Returns number of grains."""
        return self._ngrains
#
#-----------------------------------------------------------------------
#
    @ngrains.setter
    def ngrains(self, value):
        """Sets number of grains."""
        self._ngrains = value
#
#-----------------------------------------------------------------------
#
    @property
    def bounding_box(self):
        """Gets bounding box corners."""

        return self._bbox_pmin, self._bbox_pmax
#
#-----------------------------------------------------------------------
#
    @bounding_box.setter
    def bounding_box(self, value):
        """Sets the mesh bounding box.
           The bounding box is only used when writting SnappyHexMesh meshes."""

        pmin, pmax = value
        if (pmax is None) | (pmin is None):
            [pmin, pmax] = self._get_BoundingBox()

        self._bbox_pmin = pmin
        self._bbox_pmax = pmax
        self._bbox_set = True
        self._packing_done = False
#
#-----------------------------------------------------------------------
#
    @property
    def nblocks(self):
        """Gets mesh offset in x direction."""

        return self._nblocks
#
#-----------------------------------------------------------------------
#
    @nblocks.setter
    def nblocks(self, value):
        """" Set the number of blocks in each direction.
            It is used to write BlockMeshDict in PySnnapy."""
        nblocks_x = value[0]
        nblocks_y = value[1]
        nblocks_z = value[2]
        
        if self._check_nblocks(nblocks_x, nblocks_y, nblocks_z):
            self._nblocks = [nblocks_x, nblocks_y, nblocks_z]
            self._packing_done = False
        else:
            raise PoreError.ErrorNBlocks

#
#-----------------------------------------------------------------------
#
    @property
    def lx(self):
        """Gets horizontal length."""

        return self._lx
#
#-----------------------------------------------------------------------
#
    @lx.setter
    def lx(self, value):
        """" Sets the horizontal length."""
        if self._check_lx(value):
            self._lx = value
            self._packing_done = False
        else:
            raise PoreError.ErrorLx
#
#-----------------------------------------------------------------------
#
    @property
    def ly(self):
        """Gets vertical length."""

        return self._ly
#
#-----------------------------------------------------------------------
#
    @ly.setter
    def ly(self, value):
        """" Sets the vertical length."""
        if self._check_ly(value):
            self._ly = value
            self._packing_done = False
        else:
            raise PoreError.ErrorLy

#
#-----------------------------------------------------------------------
#
    @property
    def xoffset(self):
        """Gets mesh offset in x direction."""

        return self._xoffset
#
#-----------------------------------------------------------------------
#
    @xoffset.setter
    def xoffset(self, value):
        """Sets mesh offset in x and resets packing state."""
        if self._check_xoffset(value):
            self._xoffset = value
        else:
            raise PoreError.ErrorXoffset
#
#-----------------------------------------------------------------------
#
    @property
    def size(self):
        """Gets mesh size."""

        return self._size
#
#-----------------------------------------------------------------------
#
    @size.setter
    def size(self, value):
        """Sets mesh size and resets packing state."""
        #Allow a general
        # expression using, x, y, r.
        if self._check_size(value):
            self._size = value
            self._packing_done = False
        else:
            raise PoreError.ErrorSize
#
#-----------------------------------------------------------------------
#
    @property
    def zeta(self):
        """ Returns zeta coordinate"""
        return self._zeta
#
#-----------------------------------------------------------------------
#
    @property
    def circles(self):
        """Gets circles."""

        if not self._circles_done:
            self._packing_done = self._generate_packing()
        return self._circles
#
#-----------------------------------------------------------------------
#
    @circles.setter
    def circles(self, value):
        """set circles."""

        self._circles = value
#
#-----------------------------------------------------------------------
#
    @property
    def is3D(self):
        """Gets the 3D status."""

        return self._is3D
#
#-----------------------------------------------------------------------
#
    @is3D.setter
    def is3D(self, value):
        """set 3D."""

        if type(value) == bool:
            self._is3D = value
        else:
           warnings.warn("Value must be True/False.")
           self._is3D = False
          
#
#-----------------------------------------------------------------------
#
    def _generate_packing(self):
        """Defined in children"""
        pass
#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_lx(lx):
        """ Checks lenght of the domain in the horizontal direction.
            It has to be greater than 1e-9."""
        return lx > 1.e-9
#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_ly(ly):
        """ Checks lenght of the domain in the vertical direction.
            It has to be greater than 1e-9."""
        return ly > 1.e-9
#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_nblocks(nblocks_x, nblocks_y, nblocks_z):
        """ Checks the number of blocks for SnappyHexMesh.
            All of them have to be positive."""
        return nblocks_x*nblocks_y*nblocks_z > 1
#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_size(size):
        """ Checks the mesh size.
            It has to be greater than 1e-9."""
        return size > 1.e-9
#
#-----------------------------------------------------------------------
#
    # pylint: disable=W0613
    @staticmethod
    def _check_xoffset(xoffset):
        """ Checks the mesh offset in the horizontal direction.
            All values are allowed."""
        return True
#
#-----------------------------------------------------------------------
#
    # pylint: disable=W0212
    def __add__(self, other):
        """Joins two porous media. The resulting porous media is of class RecPore2D"""
        # Checks if other is a porous medium
        if other.__class__.__name__ not in [' RecPore2D', 'RegPore2D', 'RndPore2D']:

            raise PoreError.ErrorNotPorousMedium

        # Packing have to be generated to merge the media.
        if not self._packing_done:
            self._packing_done = self._generate_packing()
        if not other._packing_done:
            other._packing_done = other._generate_packing()

        if self._packing_done and other._packing_done:
                # Warns user if porous media overlap.
            if self._overlap(other):

                msg = 'Porous media overlap:\n'
            #msg = msg + 'lx1 = ' + str(self._lx) + '\n'
            #msg = msg + 'throat1 = ' + str(self._throat) + '\n'
            #msg = msg + 'total1 = ' + str(self._lx + self._throat) + '\n'
            #msg = msg + 'lx2 = ' + str(other._lx) + '\n'
            #msg = msg + 'throat2 = ' + str(other.throat) + '\n'

                warnings.warn(msg)
                
            new_pore = RecPore2D()
            #new_pore = RecPore2D.__init__()
            new_pore.ngrains = self.ngrains + other.ngrains

            newcircles = np.zeros(new_pore.ngrains, \
                dtype={'names':['x', 'y', 'z', 'r'], \
                'formats':['float64', 'float64', 'float64', 'float64']})

            newcircles[:]['x'] = np.concatenate((
                                 self.circles['x'] + self.xoffset, \
                                 other.circles['x']+ other.xoffset), axis=0)

            newcircles[:]['y'] = np.concatenate((self.circles['y'], \
                                            other.circles['y']), axis=0)

            newcircles[:]['z'] = np.concatenate((self.circles['z'], \
                                            other.circles['z']), axis=0)

            newcircles[:]['r'] = np.concatenate((self.circles['r'], \
                                            other.circles['r']), axis=0)

            new_pore.circles = newcircles
            
            new_pore.size = min([self.size, other.size])
            new_pore.is3D = self.is3D | other.is3D
            #Bounding box for the new porous media
            [pmin1, pmax1] = self.bounding_box
            [pmin2, pmax2] = other.bounding_box
            pmin = [np.min([pmin1[0] + self.xoffset, pmin2[0] + other.xoffset]),
                    np.min([pmin1[1], pmin2[1]]),
                    pmin1[2]]
            pmax = [np.max([pmax1[0] + self.xoffset, pmax2[0] + other.xoffset]),
                    np.max([pmax1[1], pmax2[1]]),
                    pmax1[2]]
            
            new_pore.bounding_box = [pmin, pmax]
            new_pore._packing_done = True
            

            return new_pore
#
#-----------------------------------------------------------------------
#

    def _overlap(self, other):
        """Checks if two porous media overlap."""

        if other.__class__.__name__ not in ['RegPore2D', 'RndPore2D']:
            raise PoreError.ErrorNotPorousMedium

        a_x1 = np.min(self.circles['x'] + self.xoffset)
        a_x2 = np.max(self.circles['x'] + self.xoffset)
        a_y1 = np.min(self.circles['y'])
        a_y2 = np.max(self.circles['y'])

        b_x1 = np.min(other.circles['x'] + other.xoffset)
        b_x2 = np.max(other.circles['x'] + other.xoffset)
        b_y1 = np.min(other.circles['y'])
        b_y2 = np.max(other.circles['y'])

        overlap = not((a_x1 > b_x2) or \
            (a_x2 < b_x1) or \
            (a_y2 < b_y1) or \
            (a_y1 > b_y2))

        return overlap
#
#-----------------------------------------------------------------------
#
    def write_mesh(self, fname='', meshtype='gmsh'):
        """ Writes the porus media for the mesh/cad program"""
        meshes = {'gmsh':self._writeGMSH, 'oscad':self._writeOPENSCAD, \
                  'snappy':self._writeSNAPPYHEXMESH, \
                  'stl': self._writeSTL}

        if not self._packing_done:
            self._packing_done = self._generate_packing()

        meshes[meshtype](fname)
#
#-----------------------------------------------------------------------
#
    def _get_BoundingBox(self):
        """Defined  by children."""
        pass
        
        
#
#-----------------------------------------------------------------------
#
    def _writeGMSH(self, fname):
        """Writes the discs packing for gmsh"""

        import PyGmsh as gmsh

        mesh = gmsh.PyGmsh()

        [pmin, pmax] = self.bounding_box

        size = self.size

        mesh.add_BoundingBox(pmin[0] +  self.xoffset, pmax[0] + self.xoffset, pmin[1], pmax[1], pmin[2], size)


        for circ in self._circles:

            center = (circ['x'] + self.xoffset, circ['y'], circ['z'])
            r = circ['r']
            mesh.add_circle(center, r, size)

        mesh.write_code(fname)
#
#-----------------------------------------------------------------------
#
    def _writeSTL(self, fname, isBinary=False, addBoundingBox=False):
        """Writes the discs as STL file"""

        import trimesh as trimesh

        if addBoundingBox:
            [pmin, pmax] = self.bounding_box
            lx = pmax[0] - pmin[0]
            ly = pmax[1] - pmin[1]
            lz = pmax[2] - pmin[2]
            mesh = trimesh.creation.box(extents=[lx, ly, lz])
            trans = np.array([pmin[0]+lx/2., pmin[1]+ly/2.,pmin[2]+lz/2.])
            mesh.apply_translation(translation=trans)

        for circ in self._circles:
            r = circ['r']
            center = (circ['x'] + self.xoffset, circ['y'], circ['z'])
            
            if self.is3D:    
                aux = trimesh.creation.icosphere(subdivisions=3, radius=r)
            else:
                aux = trimesh.creation.cylinder(radius=r, height=lz, sections=64)
            aux.apply_translation(translation=center)
            
            try:
              mesh = mesh + aux
            except:
              mesh = aux
              
        mesh.export(fname,'stl_ascii')
#
#-----------------------------------------------------------------------
#
    def _writeOPENSCAD(self, fname):
        """Writes the discs packing for OpenSCAD"""

        import PyOpenSCAD as oscad

        z = self.zeta

        mesh = oscad.PyOpenSCAD()


        for circ in self._circles:

            center = (circ['x'] + self.xoffset, circ['y'], circ['z'])
            r = circ['r']
            mesh.add_cylinder(z, r, center)

        #mesh.add_BoundingBox() #OJO QUE FALTA DEFINIRLO BIEN
        mesh.write_code(fname)
#
#-----------------------------------------------------------------------
#
    def _writeSNAPPYHEXMESH(self, fname):
        """Writes the discs packing for snappyHexMesh.
           addBoundingBox ignored."""
        

        import PySnappy as snappy

        z = self.zeta

        mesh = snappy.PySnappy()

        mesh.is3D = self.is3D
        
        for circ in self._circles:

            center = (circ['x'] + self.xoffset, circ['y'], circ['z'])
            r = circ['r']
            
            if self.is3D:
                mesh.add_sphere(r, center)
            else:
               mesh.add_cylinder(z, r, center)

        [pmin, pmax] = self.bounding_box
        
        mesh.set_bounding_box(pmin, pmax)

        mesh.set_number_of_blocks(self.nblocks[0], self.nblocks[1],
                                  self.nblocks[2])

        # Gets a point inside the mesh
        point_inside_circle = True
        p1z = self._zeta

        while point_inside_circle:
            
            p1x =  np.random.uniform(pmin[0], pmax[0])
            p1y =  np.random.uniform(pmin[1], pmax[1])
            point_inside_circle = False

            for circ in self._circles:
                center = (circ['x'] + self.xoffset, circ['y'], circ['z'])
                d = np.sqrt((center[0]-p1x)**2. + (center[1]-p1y)**2.)
                if d<circ['r']:
                    point_inside_circle = True
                    break

        print [p1x, p1y, p1z]
        mesh.point_inside = [p1x, p1y, p1z]

        mesh.write_code(fname)
#
#-----------------------------------------------------------------------
# END class RecPore2D
#-----------------------------------------------------------------------
#

class RegPore2D(RecPore2D):
    """Regular porous medium
       Pore throat, lx (length) and ly (height)
        are computed according to the packing."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, nx=2, ny=2, radius=0.1, throat=0.1, packing='sqr'):
        """Checks arguments and creates the packing of discs."""

        #RecPore2D.__init__(self)
        super(RegPore2D, self).__init__()
        self._packs = ['tri', 'sqr', 'etri']
        self._radius = None
        self._throat = None
        # To avoid error during initialization because of the call to
        # _compute_number_of_grains inside nx.setter and ny.setter
        # we dont use the setters. Possible design mistake.
        self._nx = nx
        self._ny = ny

        self.packing = packing
        self.radius = radius
        self.throat = throat
        self.lx = self._compute_lx()
        self.ly = self._compute_ly()
        self.ngrains = self._compute_number_of_grains()
        self.size = 0.8*self._throat
#
#-----------------------------------------------------------------------
#
    @property
    def radius(self):
        """Gets radius."""
        return self._radius
#
#-----------------------------------------------------------------------
#
    @radius.setter
    def radius(self, value):
        """Set radius """
        if self._check_radius(value):
            self._radius = value
            self._packing_done = False
        else:
            raise PoreError.ErrorRadius
#
#-----------------------------------------------------------------------
#
    @property
    def throat(self):
        """Gets throat."""
        return self._throat
#
#-----------------------------------------------------------------------
#
    @throat.setter
    def throat(self, value):
        """Set throat."""
        if self._check_throat(value):
            self._throat = value
            self._packing_done = False
            self.lx = self._compute_lx()
            self.ly = self._compute_ly()
        else:
            raise PoreError.ErrorThroatNegative
#
#-----------------------------------------------------------------------
#
    @property
    def nx(self):
        """Gets nx."""
        return self._nx
#
#-----------------------------------------------------------------------
#
    @nx.setter
    def nx(self, value):
        """Set nx."""
        if self._check_nx(value):
            self._nx = value
            self.ngrains = self._compute_number_of_grains()
            self.lx = self._compute_lx()
            self._packing_done = False
        else:
            raise PoreError.ErrorNx
#
#-----------------------------------------------------------------------
#
    @property
    def ny(self):
        """Gets nx."""
        return self._ny
#
#-----------------------------------------------------------------------
#
    @ny.setter
    def ny(self, value):
        """Set ny."""
        if self._check_ny(value):
            self._ny = value
            self.ngrains = self._compute_number_of_grains()
            self.ly = self._compute_ly()
            self._packing_done = False
        else:
            raise PoreError.ErrorNy
#
#-----------------------------------------------------------------------
#
    @property
    def packing(self):
        """Gets packing."""
        return self._packing
#
#-----------------------------------------------------------------------
#
    @packing.setter
    def packing(self, value):
        """Set nx."""
        if self._check_packing(value):
            self._packing = value
            self._packing_done = False
        else:
            raise PoreError.ErrorPacking

#-----------------------------------------------------------------------
#
    def _check_packing(self, packing):
        """Checks if the packing is valid
        The only allowed packings are:
            tri -- triangular
            sqr  -- square
            etri -- elongated triangular
        """

        return packing in self._packs
#
#-----------------------------------------------------------------------
#
    def _check_nx(self, nx):
        """Checks if the number of grains in the x direction
           is positive."""

        nx_ok = False

        if nx > 0:
            if (self.packing != 'sqr' and nx % 2 != 0) \
                or self.packing == 'sqr':
                nx_ok = True

        return nx_ok
#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_ny(ny):
        """Checks if the number of grains in the y direction
           is positive and that ny*radius<1.0."""

        return ny > 0
#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_radius(radius):
        """Checks if the grain radius is greater than 1.0e-9"""

        return radius > 1.0e-9

#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_throat(throat):
        """Checks if the pore throat is greater than 1.0e-9"""

        return throat > -1.0e-9

#
#-----------------------------------------------------------------------
#
    def _compute_lx(self):
        """Computes the lenght of the system in the x
           direction according to the packing and the geometry"""

        if self.packing == 'tri' or self.packing == 'etri':
            # old lx. 99% sure it is wrong.
            #lx = (3.0*self.nx + 1.0)*self.throat \
            #    + 2.0*self.radius*(2.0*self.nx+1.0)
            lx = (self.nx - 1.0)*self.throat \
                + 2.0*self.nx*self.radius
        elif self.packing == 'sqr':
            lx = (self.nx + 1.0)*self.throat \
                + 2.0*self.nx*self.radius

        elif self.packing == 'rnd':
            #lx = self.nx*self.radius
            print "que hago aqui?"

        return lx

#
#-----------------------------------------------------------------------
#
    def _compute_ly(self):
        """Computes the lenght of the system in the y
           direction according to the packing and the geometry"""


        if self.packing == 'rnd':
            ly = 2.*self._ny*self._radius
            print "que hago aqui?"
        else:
            ly = self._ny*(self._throat + 2.*self._radius)
            
        return ly
#
#-----------------------------------------------------------------------
#
    def _compute_throat(self):
        """Computes throat from ny, ly, and radius"""

        throat = (self._ly - (2.0*self._ny*self._radius))/(self._ny + 1)
        return throat
#
#-----------------------------------------------------------------------
#

    def _generate_packing(self):
        """ Generates the position of the grains"""

        if self.packing == 'tri':
            self.circles, self._circles_done = self._pack_tri()

        elif self.packing == 'sqr':
            self.circles, self._circles_done = self._pack_sqr()

        elif self.packing == 'etri':
            self.circles, self._circles_done = self._pack_etri()

        if None in self.bounding_box:
            self.bounding_box = self._get_BoundingBox()
            
        #print 'max'
        #print np.max(self.circles[:]['x'])*0.02
        #print np.max(self.circles[:]['y'])*0.02
        #print 'min'
        #print np.min(self.circles[:]['x'])*0.02
        #print np.min(self.circles[:]['y'])*0.02
        return True

#
#-----------------------------------------------------------------------
#
    # pylint: disable=E1101
    def _pack_sqr(self):
        """ Generates the coordinates of the grain centers
            for the square packing"""

        i = np.arange(1, self._nx + 1)
        xi = i*self._throat + (2.0*i -1.0)*self._radius

        j = np.arange(1, self._ny + 1)
        yj = j*self._throat + (2.0*j -1.0)*self._radius


        circles = np.zeros(self._ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})

        circles[:]['x'] = xi.repeat(self._ny)
        circles[:]['y'] = np.tile(yj, self._nx)
        circles[:]['z'] = np.tile(self.zeta, self._ngrains)
        circles[:]['r'] = np.tile(self._radius, self._ngrains)

        return circles, True

#
#-----------------------------------------------------------------------
#
    def _pack_tri(self):
        """ Generates the coordinates of the grain centers
            for the tri packing"""

        i = np.arange(1, self.nx + 1)
        xi = i*self.throat + (2.0*i -1.0)*self.radius

        j_odd = np.arange(1, self._ny+1)
        yj_odd = j_odd*self.throat + (2.0*j_odd -1.0)*self.radius

        j_even = np.arange(1, self.ny)
        yj_even = j_even*(self.throat + 2.0*self.radius) + self.throat/2.0
        yj = np.hstack((yj_odd, yj_even))


        xrep = np.ones(self.nx, dtype=np.int)
        xrep[::2] = self.ny*xrep[::2] #odd
        xrep[1::2] = (self.ny-1)*xrep[1::2] #even

        circles = np.zeros(self.ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})

        # If nx is odd, we need one more yj_odd column.
        y_aux = np.tile(yj, self.nx/2)
        if self.nx% 2> 0:
            y_aux = np.hstack((y_aux, yj_odd))
            
        circles[:]['x'] = xi.repeat(xrep)
        circles[:]['y'] = y_aux
        circles[:]['z'] = np.tile(self.zeta, self._ngrains)
        circles[:]['r'] = np.tile(self._radius, self._ngrains)


        return circles, True
#
#-----------------------------------------------------------------------
#

    def _pack_etri(self):
        """ Generates the coordinates of the grains' centers
            for the elongated triangular packing"""

        i = np.arange(1, self._nx + 1)
        xi = i*self._throat + (2.0*i -1.0)*self._radius

        j = np.arange(1, self._ny + 1)
        yj = j*self._throat + (2.0*j -1.0)*self._radius


        circles = np.zeros(self._ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})


        circles[:]['x'] = xi.repeat(self._ny)
        circles[:]['y'] = np.tile(yj, self._nx)
        circles[:]['z'] = np.tile(self.zeta, self._ngrains)
        circles[:]['r'] = np.tile(self._radius, self._ngrains)


        return circles, True
#
#-----------------------------------------------------------------------
#
    def _compute_number_of_grains(self):

        """Computes number of grains according to the packing"""

        if (self.packing == 'sqr') | (self.packing == 'etri'):
            ngrains = self.nx*self.ny

        else:
            if self.nx%2==0:
                ngrains = (self.nx/2)*(self.ny - 1) + (self.nx/2)*(self.ny)
            else:
                ngrains = (self.nx/2)*(self.ny - 1) + (self.nx/2 + 1)*(self.ny)

        return ngrains
#
#-----------------------------------------------------------------------
#
    def _get_BoundingBox(self):
        """Gets mesh bounding box."""

        if self.circles is not None:
            xmin = np.min(self.circles[:]['x'] - self.circles[:]['r'])
            xmax = np.max(self.circles[:]['x'] + self.circles[:]['r'])
            ymin = np.min(self.circles[:]['y'] - self.circles[:]['r'])
            ymax = np.max(self.circles[:]['y'] + self.circles[:]['r'])
            rmax = np.max(self.circles[:]['r'])
            zmin = self.zeta - rmax
            zmax = self.zeta + rmax

            pmin = [xmin - self.throat, ymin - self.throat, zmin]
            pmax = [xmax + self.throat, ymax + self.throat, zmax]
        else:
            pmin = None
            pmax = None

        return  [pmin, pmax]

    
#
#-----------------------------------------------------------------------
# END class RegPore2D
#-----------------------------------------------------------------------
#

class RndPore2D(RecPore2D):
    """Random porous medium."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, lx=1., ly=1., rmin=0.01, rmax=0.2, target_porosity=0.5, packing='rnd'):
        """Chaks arguments and creates random packing of discs."""

        #RecPore2D.__init__(self)
        super(RndPore2D, self).__init__()

        self._packs = ['rnd'] #TO DO Jodry-Tory, etc.
        self._rmin = None
        self._rmax = None
        self._target_porosity = None
        self._packing = None
        self._ntries_max = None
        self._ngrains_max = None
        self._tolerance = rmin/10.

        self.lx = lx
        self.ly = ly
        self.rmin = rmin
        self.rmax = rmax
        self.target_porosity = target_porosity
        self.packing = packing
        self.ntries_max = int(1e7)
        self.ngrains_max = 1000
        #self.distribution = TO DO
#
#-----------------------------------------------------------------------
#

    @property
    def rmin(self):
        """ Returns minimun radius of the packing."""
        return self._rmin
#
#-----------------------------------------------------------------------
#
    @rmin.setter
    def rmin(self, value):
        """ Sets minimun grain radius of the packing."""
        if self._check_rmin(value):
            self._rmin = value
            self._packing_done = False
        else:
            raise PoreError.ErrorRmin

#
#-----------------------------------------------------------------------
#
    @property
    def rmax(self):
        """ Returns maximun radius of the packing."""
        return self._rmax
#
#-----------------------------------------------------------------------
#
    @rmax.setter
    def rmax(self, value):
        """ Sets maximun grain radius of the packing."""
        if self._check_rmax(value):
            self._rmax = value
            self._packing_done = False
        else:
            raise PoreError.ErrorRmax

#
#-----------------------------------------------------------------------
#
    @property
    def target_porosity(self):
        """ Returns target porosity of the packing."""
        return self._target_porosity
#
#-----------------------------------------------------------------------
#
    @target_porosity.setter
    def target_porosity(self, value):
        """ Sets target porosity of the packing."""
        if self._check_porosity(value):
            self._target_porosity = value
            self._packing_done = False
        else:
            raise PoreError.ErrorPorosity

#
#-----------------------------------------------------------------------
#
    @property
    def ntries_max(self):
        """ Returns number of maximum consecutive unsuccessful tries
            to add a new grain to the packing."""
        return self._ntries_max
#
#-----------------------------------------------------------------------
#
    @ntries_max.setter
    def ntries_max(self, value):
        """ Sets maximun number of consecutive tries to add a new grain."""

        if self._check_ntries_max(value):
            self._ntries_max = value
            self._packing_done = False
        else:
            raise PoreError.ErrorNtriesMax
#
#-----------------------------------------------------------------------
#
    @property
    def ngrains_max(self):
        """ Returns number of maximum number of grains of the packing."""
        return self._ngrains_max
#
#-----------------------------------------------------------------------
#
    @ngrains_max.setter
    def ngrains_max(self, value):
        """ Sets maximun number of grains of the packing."""
        if self._check_ngrains_max(value):
            self._ngrains_max = value
            self._packing_done = False
        else:
            raise PoreError.ErrorNgrainsMax
#
#-----------------------------------------------------------------------
#
    @property
    def packing(self):
     return self._packing
#
#-----------------------------------------------------------------------
#
    @packing.setter
    def packing(self, value):
        """ Sets the packing."""
        # TODO: Check packing
        self._packing = value
#
#-----------------------------------------------------------------------
#
    @property
    def tolerance(self):
     return self._tolerance
#
#-----------------------------------------------------------------------
#
    @tolerance.setter
    def tolerance(self, value):
        """ Sets the tolerance."""
        # TODO: Check tolerance
        self._tolerance = value
#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_rmin(rmin):
        """ Checks minimum grain radius."""
        return rmin > 1.e-9

#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_rmax(rmax):
        """ Checks maximum grain radius."""
        return rmax > 1.e-9

#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_porosity(porosity):
        """ Checks porosity. It must be greater than zero."""
        return porosity > 1.e-9

#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_ntries_max(ntries_max):
        """ Checks maximum number of attempts to add a new grain.
            It must be an integer greater than zero."""
        return isinstance(ntries_max, int) and ntries_max > 1

#
#-----------------------------------------------------------------------
#
    @staticmethod
    def _check_ngrains_max(ngrains_max):
        """ Checks maximum number of grains.
            It must be an integer greater than zero."""
        return isinstance(ngrains_max, int) and ngrains_max > 1

#
#-----------------------------------------------------------------------
#
    def _generate_packing(self):
        """ Generates the position of the grains."""

        if self.packing == 'rnd':
            print "entro en rnd pack"
            self.circles, self.ngrains, self._circles_done = self._pack_rnd()

        if None in self.bounding_box:
            self.bounding_box = self._get_BoundingBox()

        return True
#
#-----------------------------------------------------------------------
#
    def _pack_rnd(self):
        """ Generates the grains for a random packing."""
        
        porosity = 1.0
        ntries = 0
        ngrains = 0
        grains = []
        rg = []
        
        from PyGrain import Grain as grain

        while porosity > self.target_porosity and \
              ntries < self.ntries_max and \
              ngrains < self.ngrains_max:

            new_grain = grain(rmin=self.rmin, rmax=self.rmax, \
                              lx=self.lx, ly=self.ly, \
                              tolerance=self.tolerance)

            if (new_grain.overlap_grains(grains)) or \
               new_grain.overlap_rectangle([0.,0.] ,[self.lx, self.ly]):

                ntries = ntries + 1
                
            else:

                grains.append(new_grain)
                ntries  = 0
                ngrains = ngrains + 1
                porosity = porosity - new_grain.area/(self.lx*self.ly)
                rg = []

    
        print "ngrains = %d (max= %d)" %(ngrains, self.ngrains_max)
        print "porosity = %g (target = %g)" %(porosity, self.target_porosity)
        print "ntries = %d (max= %d)" %(ntries, self.ntries_max)
        
        circles = np.zeros(ngrains, \
            dtype={'names':['x', 'y', 'z', 'r'], \
            'formats':['float64', 'float64', 'float64', 'float64']})

        circles[:]['x'] = np.fromiter((grain.x for grain in grains), \
                                      dtype='float64')
        circles[:]['y'] = np.fromiter((grain.y for grain in grains), \
                                      dtype='float64')
        circles[:]['z'] = np.tile(self.zeta, ngrains)
        circles[:]['r'] = np.fromiter((grain.radius for grain in grains), \
                                       dtype='float64')
        
        return circles, ngrains, True
 #
#-----------------------------------------------------------------------
#   
    def _get_BoundingBox(self):
        """Gets mesh bounding box."""

        if self.circles is not None:
            xmin = np.min(self.circles[:]['x'] - self.circles[:]['r'])
            xmax = np.max(self.circles[:]['x'] + self.circles[:]['r'])
            ymin = np.min(self.circles[:]['y'] - self.circles[:]['r'])
            ymax = np.max(self.circles[:]['y'] + self.circles[:]['r'])
            rmax = np.max(self.circles[:]['r'])
            rmin = np.min(self.circles[:]['r'])
            zmin = self.zeta - rmax
            zmax = self.zeta + rmin
            pmin = [xmin, ymin, zmin]
            pmax = [xmax, ymax, zmax]
        else:
            pmin = None
            pmax = None

        return  [pmin, pmax]
#
#-----------------------------------------------------------------------
# END class RndPore2D
#-----------------------------------------------------------------------
#
