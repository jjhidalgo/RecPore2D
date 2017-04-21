"""Module to write porous medium generated with
    RegPore2D in SnappyHexMesh format"""

class PySnappy(object):
    """SnappyHexMesh wrapper."""
#
#-----------------------------------------------------------------------
#
    def __init__(self):
        """Just creates empty arrays"""

        self.cubes = []
        self.cylinders = []
        self.spheres = []
        self.bbox = None
        self._is3D = False
        self.__bbox_set = False
        self.nblocks = [400, 400, 1]
        self.grading = [1, 1, 1]
        self.point_inside = [0., 0., 0.]
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
            self.nblocks[2] = 1 + 399*value
        else:
           warnings.warn("Value must be True/False.")
           self._is3D = False

#
#-----------------------------------------------------------------------
#
    def add_cylinder(self, height, radius, center=None):
        """" Adds one cylinder to the mesh."""
        from PySnappy import SnappyCylinder as sc

        cylinder = sc(height, radius, center)
        self.cylinders.append(cylinder)

        return cylinder

#
#-----------------------------------------------------------------------
#
    def add_sphere(self, radius, center=None):
        """" Adds one sphere to the mesh."""
        from PySnappy import SnappySphere as ssph

        sphere = ssph(radius, center)
        self.spheres.append(sphere)

        return sphere
#
#-----------------------------------------------------------------------
#
    def add_cube(self, size, center=None):
        """" Adds one cube to the mesh."""
        from PySnappy import SnappyBox as sbox

        cube = sbox(size, center)
        self.cubes.append(cube)

        return cube
#
#-----------------------------------------------------------------------
#
    def set_bounding_box(self, point1, point2):
        """" Adds a bounding box. It used to write BlockMeshDict."""

        self.bbox = [point1, point2]
        self.__bbox_set = True

#
#-----------------------------------------------------------------------
#
    def set_number_of_blocks(self, nblocks_x, nblocks_y, nblocks_z):
        """" Set the number of blocks in each direction.
            It used to write BlockMeshDict."""

        self.nblocks = [nblocks_x, nblocks_y, nblocks_z]

#
#-----------------------------------------------------------------------
#
    def set_grading(self, gradx, grady, gradz):
        """" Set the block grading in each direction.
        It used to write BlockMeshDict."""
        self.grading = [gradx, grady, gradz]
#
#-----------------------------------------------------------------------
#
    def __get_point_inside(self):
        """" Gets a point inside the mesh.
             The point is a distance 1e-5 to the right
             of the first grain."""
        
#TO DO: Check that it is not inside another grain.

        center1 = self.cylinders[0].center
        radius = self.cylinders[0].radius

        #x_in = center1[0] + radius
        #y_in = center1[2] + radius
        #z_in = center1[2]

        x_in = center1[0] + radius + 0.00001
        y_in = center1[1]
        z_in = center1[2]

        return [x_in, y_in, z_in]
#
#-----------------------------------------------------------------------
#
    def write_code(self, fname):
        """Writes the mesh in SnappyHexMesh format."""
        grains_code = [""]
        refsurf_code = [""]
        igrain = 0

        grain_template_str = '\n'.join(['grain$grainid', '{', '$cnt', '}', ''])

        import os
        from string import Template

        grain_tmpl = Template(grain_template_str)

        for sphere in self.spheres:
            igrain = igrain + 1
            grains_code.append(grain_tmpl.substitute(
                grainid=igrain,
                cnt=sphere.code()))

        for cylinder in self.cylinders:
            igrain = igrain + 1
            grains_code.append(grain_tmpl.substitute(
                grainid=igrain,
                cnt=cylinder.code()))


        for cube in self.cubes:
            igrain = igrain + 1
            grains_code.append(grain_tmpl.substitute(
                grainid=igrain,
                cnt=cube.code()))

        ngrains = igrain

        for igrain in xrange(1, ngrains + 1):
            refsurf_code.append(grain_tmpl.substitute(
                grainid=igrain,
                cnt='level (2 2);'))

        # point inside a cell
        p_inside = self.point_inside


        import pkg_resources as pkg_r
        snappy_tmpl_file = pkg_r.resource_string('PySnappy','snappy.tmpl')
        
        
        #snappy_tmpl_file = open('snappy.tmpl')

        #snappy_tmpl_file = open(pkg_path)
        #snappy_tmpl = Template(snappy_tmpl_file.read())
        snappy_tmpl = Template(snappy_tmpl_file)
        snappy_code = snappy_tmpl.substitute(
            grains=''.join(grains_code),
            refinementsurfaces=''.join(refsurf_code),
            refinementRegions=''.join(' '),
            loc1=p_inside[0],
            loc2=p_inside[1],
            loc3=p_inside[2])

        if fname == '':
            fname = 'snappyHexMeshDict'

        snappy_file = open(fname, "w")
        snappy_file.write(''.join(snappy_code))
        snappy_file.close()

        if self.__bbox_set:

            import pkg_resources as pkg_r
            blockmesh_tmpl_file = pkg_r.resource_string('PySnappy','blockMeshDict.tmpl')

            #blockmesh_tmpl_file = open('blockMeshDict.tmpl')
            if self.is3D:
                gr_cl_type = "wall"
            else:
                gr_cl_type = "empty"
            
            blockmesh_tmpl = Template(blockmesh_tmpl_file)
            blockmesh_code = blockmesh_tmpl.substitute(
                nx=self.nblocks[0],
                ny=self.nblocks[1],
                nz=self.nblocks[2],
                gradx=self.grading[0],
                grady=self.grading[1],
                gradz=self.grading[2],
                x1=self.bbox[0][0],
                y1=self.bbox[0][1],
                z1=self.bbox[0][2],
                x2=self.bbox[1][0],
                y2=self.bbox[1][1],
                z2=self.bbox[1][2],
                groundtype=gr_cl_type,
                ceilingtype=gr_cl_type),

            fname = 'blockMeshDict'

            geo_file = open(fname, "w")
            geo_file.write(''.join(blockmesh_code))
            geo_file.close()

#
#-----------------------------------------------------------------------
# END class PySnappy
#-----------------------------------------------------------------------
#
class SnappyObject(object):
    """This class creates a generic Snappy object.
       (limited to cubes, spheres, cylinders or polygons)"""

#
#-----------------------------------------------------------------------
#
    def __init__(self):
        """To be redefined in children."""
        self.center = None

#
#-----------------------------------------------------------------------
#
    def code(self,):
        """To be redefined in children."""
        pass

#
#-----------------------------------------------------------------------
# END class SnappyObject
#-----------------------------------------------------------------------
#

class SnappyCylinder(SnappyObject):
    """This class creates and writes code for a cylinder in
        SnappyHexMesh format."""

#
#-----------------------------------------------------------------------
#
    def __init__(self, height, radius, center=None):
        """Creates a cylinder."""
        SnappyObject.__init__(self)
        self.height = height
        self.radius = radius
        self.center = center

#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a cylinder SnappyHexMesh format."""

        from string import Template

        cylinder_template_string = ';\n'.join(
            ['  type searchableCylinder',
             '    point1 ($x1 $y1 $z1)',
             '    point2 ($x2 $y2 $z2)',
             '    radius $radius',
             ''])

        cylinder_tmpl = Template(cylinder_template_string)

        cylinder_code = cylinder_tmpl.substitute(
            x1=self.center[0],
            y1=self.center[1],
            z1=self.center[2],
            x2=self.center[0],
            y2=self.center[1],
            z2=self.center[2] + self.height,
            radius=self.radius)

        return cylinder_code

#
#-----------------------------------------------------------------------
# END class SnappyCylinder
#-----------------------------------------------------------------------
#


class SnappySphere(SnappyObject):
    """This class creates and writes code for a sphere
       in SnappyHexMesh format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, radius, center=None):
        """Creates a sphere."""
        SnappyObject.__init__(self)
        self.radius = radius
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a sphere SnappyHexMesh format."""

        from string import Template
        sphere_template_string = ';\n'.join(
            ['  type searchableSphere',
             '    centre ($x1 $y1 $z1)',
             '    radius $radius',
             ''])

        sphere_tmpl = Template(sphere_template_string)

        sphere_code = sphere_tmpl.substitute(
            x1=self.center[0],
            y1=self.center[1],
            z1=self.center[2],
            radius=self.radius)

        return sphere_code

#
#-----------------------------------------------------------------------
# END class SnappySphere
#-----------------------------------------------------------------------
#


class SnappyBox(SnappyObject):
    """This class creates and writes code for a sphere
    in SnappyHexMesh format."""

#
#-----------------------------------------------------------------------
#
    def __init__(self, size, center=None):
        """Creates a box."""
        SnappyObject.__init__(self)
        self.size = size
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a cube in SnappyHexMesh format."""

        from string import Template
        box_template_string = ';\n'.join(
            ['  type searchableBox',
             '    min ($x1 $y1 $z1)',
             '    max ($x2 $y2 $z2)'
             ''])

        box_tmpl = Template(box_template_string)

        box_code = box_tmpl.substitute(
            x1=self.center.x - self.size/2.,
            y1=self.center.y - self.size/2.,
            z1=self.center.z - self.size/2.,
            x2=self.center.x + self.size/2.,
            y2=self.center.y + self.size/2.,
            z2=self.center.z + self.size/2.)

        return box_code

#
#-----------------------------------------------------------------------
# END class SnappyBox
#-----------------------------------------------------------------------
#
