"""Module to write porus mediim generated with
   RegPore2D in OpenSCAD format"""

class PyOpenSCAD(object):
    """OpenSCAD wrapper."""

#
#-----------------------------------------------------------------------
#
    def __init__(self):
        """Just creates empty arrays"""

        self.cubes = []
        self.cylinders = []
        self.spheres = []

#
#-----------------------------------------------------------------------
#
    def add_cylinder(self, height, radius, center=None):
        """" Adds one cylinder to the mesh."""
        from PyOpenSCAD import OpenScadCylinder as oc

        cylinder = oc(height, radius, center)
        self.cylinders.append(cylinder)

        return cylinder

#
#-----------------------------------------------------------------------
#
    def add_sphere(self, radius, center=None):
        """" Adds one sphere to the mesh."""
        from PyOpenSCAD import OpenScadSphere as osph

        sphere = osph(radius, center)
        self.spheres.append(sphere)

        return sphere
#
#-----------------------------------------------------------------------
#
    def add_cube(self, size, center=None):
        """" Adds one cube to the mesh."""
        from PyOpenSCAD import OpenScadCube as ocube

        cube = ocube(size, center)
        self.cubes.append(cube)

        return cube
#
#-----------------------------------------------------------------------
#
    def write_code(self, fname):
        """Writes the mesh in OpenScad format."""
        oscad_code = [""]

        for sphere in self.spheres:

            oscad_code.append(sphere.code())

        for cylinder in self.cylinders:
            oscad_code.append(cylinder.code())

        for cube in self.cubes:
            oscad_code.append(cube.code())

        if fname == '':
            fname = 'untitled.scad'

        geo_file = open(fname, "w")
        geo_file.write(''.join(oscad_code))
        geo_file.close()

#
#-----------------------------------------------------------------------
# END class PyOpenSCAD
#-----------------------------------------------------------------------
#
class OpenScadObject(object):
    """This class creates a generic openSCAD object.
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
#
    def translate_code(self, code_in):
        """Wrapps code in a translate environment."""

        center = ','.join(map(str, self.center))

        code = 'translate([{:}])'.format(center)
        code += code_in

        return code


#
#-----------------------------------------------------------------------
# END class OpenScadObject
#-----------------------------------------------------------------------
#

class OpenScadCylinder(OpenScadObject):
    """This class creates and writes code for a cylinder in openSCAD format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, height, radius, center=None):
        """Creates a cylinder."""
        OpenScadObject.__init__(self)
        self.height = height
        self.radius = radius
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a cylinder openSCAD format."""

        cylinder_code = 'cylinder(h={:.9f},r={:.9f})'.format(
            self.height, self.radius)

        if self.center != None:
            cylinder_code = self.translate_code(cylinder_code)

        return cylinder_code + '; \n'

#
#-----------------------------------------------------------------------
# END class OpenScadCylinder
#-----------------------------------------------------------------------
#


class OpenScadSphere(OpenScadObject):
    """This class creates and writes code for a sphere in openSCAD format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, radius, center=None):
        """Creates a sphere."""
        OpenScadObject.__init__(self)
        self.radius = radius
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a sphere openSCAD format."""

        sphere_code = 'sphere(r={:.9f})'.format(self.radius)

        if self.center != None:
            sphere_code = self.translate_code(sphere_code)

        return sphere_code + '; \n'

#
#-----------------------------------------------------------------------
# END class OpenScadSphere
#-----------------------------------------------------------------------
#


class OpenScadCube(OpenScadObject):
    """This class creates and writes code for a sphere in openSCAD format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, size, center=None):
        """Creates a cube."""
        OpenScadObject.__init__(self)
        self.size = size
        self.center = center
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a cube in openSCAD format."""

        cube_code = 'cube(size={:.9f})'.format(self.size)

        if self.center != None:
            cube_code = self.translate_code(cube_code)

        return cube_code + '; \n'

#
#-----------------------------------------------------------------------
# END class OpenScadCube
#-----------------------------------------------------------------------
#
