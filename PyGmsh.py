"""Gmsh wrapper. Some ideas are taken from python4gmsh by nschloe
       https://github.com/nschloe/python4gmsh/tree/master/python4gmsh"""
import numpy as np

class PyGmsh(object):
    """Gmsh wrapper to write porous media generated with RegPor2D"""
#
#-----------------------------------------------------------------------
#
    def __init__(self):
        """Just creates empty arrays"""

        self.Points = []
        self.Lines = []
        self.LineLoops = []
        self.PlaneSurface = []
        self.Physicals = []
        self.BoundingBox = []
        self._id_Points = 0
        self._id_Lines = 0 #Also for arcs.
        self._id_LineLoops = 0
        self._id_PlaneSurfaces = 0
        self._id_Physicals = 0


#
#-----------------------------------------------------------------------
#
    def add_point(self, x, y, z, size):
        """" Adds one point to the mesh"""
        from PyGmsh import gmshPoint as gp

        self._id_Points = self._id_Points + 1

        point = gp(self._id_Points, x, y, z, size)
        self.Points.append(point)

        return point

#
#-----------------------------------------------------------------------
#
    def add_circle(self, center, radius, size):
        """" Adds one circle to the mesh. A circle is made of
             5 points (the center plus 4 more) and 4 arcs.
             The circle is the added as a line loop.
             Finally the circle is added to the Physical Surface
             called grains to defien boundary conditions."""

        center = self.add_point(center[0], center[1], center[2], size)

        dx = radius*np.cos(np.pi/4.0)
        dy = radius*np.sin(np.pi/4.0)

        z = center.z

        x = center.x + dx
        y = center.y + dy
        p1 = self.add_point(x, y, z, size)

        x = center.x - dx
        y = center.y + dy
        p2 = self.add_point(x, y, z, size)

        x = center.x - dx
        y = center.y - dy
        p3 = self.add_point(x, y, z, size)

        x = center.x + dx
        y = center.y - dy
        p4 = self.add_point(x, y, z, size)

        center_id = center.point_id
        p1_id = p1.point_id
        p2_id = p2.point_id
        p3_id = p3.point_id
        p4_id = p4.point_id

        # Adds arcs and line loop
        arc1 = self.add_line((p1_id, center_id, p2_id), linetype='circle')
        arc2 = self.add_line((p2_id, center_id, p3_id), linetype='circle')
        arc3 = self.add_line((p3_id, center_id, p4_id), linetype='circle')
        arc4 = self.add_line((p4_id, center_id, p1_id), linetype='circle')

        lineloop = self.add_lineloop((arc1.line_id, arc2.line_id, \
            arc3.line_id, arc4.line_id))

        grain_phys = self.find_physical("grains")
        #import pdb; pdb.set_trace()

        ids = [line_id + 1 for line_id in lineloop.ids]

        if grain_phys == None:
            self.add_physical("grains", ids, 'surf')

        else:
            grain_phys.add_lineloop(ids)


        return
#
#-----------------------------------------------------------------------
#
    def add_line(self, p_ids, linetype='line'):
        """Adds one line to the mesh."""

        from PyGmsh import gmshLine as gl

        self._id_Lines = self._id_Lines + 1
        line = gl(self._id_Lines, p_ids, linetype)
        self.Lines.append(line)

        return line
#
#-----------------------------------------------------------------------
#
    def add_lineloop(self, line_ids):
        """Adds one line loop to the mesh.
           The line loop is added to the plane surface list."""

        from PyGmsh import gmshLineLoop as gll
        from PyGmsh import gmshPlaneSurface as gps

        self._id_LineLoops = self._id_LineLoops + 1
        lineloop = gll(self._id_LineLoops, line_ids)
        self.LineLoops.append(lineloop)

        self._id_PlaneSurfaces = self._id_PlaneSurfaces + 1
        if self._id_PlaneSurfaces < 2:
            planesurface = gps(self._id_PlaneSurfaces, lineloop.lineloop_id)
            self.PlaneSurface.append(planesurface)
        else:
            for planesurf in self.PlaneSurface:
                planesurf.add_lineloop(lineloop.lineloop_id)

        return lineloop
#
#-----------------------------------------------------------------------
#
    def add_physical(self, name, ids, phystype):
        """ Adds a physical surface to the mesh."""

        self._id_Physicals = self._id_Physicals + 1

        from PyGmsh import gmshPhysical as gphys

        phys = gphys(self._id_Physicals, name, ids, phystype)
        self.Physicals.append(phys)

        return phys
#
#-----------------------------------------------------------------------
#
    def find_physical(self, name):
        """ Returns id of the physical surface called name"""

        phys_out = None
        for phys in self.Physicals:
            if phys.name == name:
                phys_out = phys

        return phys_out
#
#-----------------------------------------------------------------------
#
    def add_BoundingBox(self, xmin, xmax, ymin, ymax, z, size):
        """Adds the points,  lines,  line loops,
           and physical surfaces of the bounding box."""

        p1 = self.add_point(xmin, ymin, z, size)
        p2 = self.add_point(xmax, ymin, z, size)
        p3 = self.add_point(xmax, ymax, z, size)
        p4 = self.add_point(xmin, ymax, z, size)

        l1 = self.add_line((p1.point_id, p2.point_id), linetype='line')
        l2 = self.add_line((p2.point_id, p3.point_id), linetype='line')
        l3 = self.add_line((p3.point_id, p4.point_id), linetype='line')
        l4 = self.add_line((p4.point_id, p1.point_id), linetype='line')

        lineloop = self.add_lineloop((-l3.line_id, -l2.line_id, \
            -l1.line_id, -l4.line_id))

        physsurf = self.add_physical('front', [0], 'surf')
        physsurf = self.add_physical('internal', [1], 'vol')
        physsurf = self.add_physical('top', [2], 'surf')
        physsurf = self.add_physical('right', [3], 'surf')
        physsurf = self.add_physical('bottom', [4], 'surf')
        physsurf = self.add_physical('left', [5], 'surf')

#
#-----------------------------------------------------------------------
#
    def write_code(self, fname):
        """Writes the mesh in gmsh geo format."""
        geo_code = [""]

        for point in self.Points:

            geo_code.append(point.code())

        for line in self.Lines:
            geo_code.append(line.code())

        for lineloop in self.LineLoops:
            geo_code.append(lineloop.code())


        for psurf in self.PlaneSurface:
            geo_code.append(psurf.code())

        auxcode = """Recombine Surface{1};
out[] = Extrude {0,  0,  1.0} {
        Surface{1};
        Layers{1};
        Recombine;
       };\n"""

        geo_code.append(auxcode)

        for phys in self.Physicals:
            geo_code.append(phys.code())

# The physical surface for the back of the box corresponds to
# plane surface 1 (it does not fit in the Physicals object
# which is assumed to be composed of lineloops).

        auxcode = "Physical Surface(\"back\") = {1};\n"
        geo_code.append(auxcode)

        if fname == '':
            fname = 'untitled.geo'

        geo_file = open(fname, "w")
        geo_file.write(''.join(geo_code))
        geo_file.close()

#
#-----------------------------------------------------------------------
# END class PyGmsh
#-----------------------------------------------------------------------
#

class gmshPoint(object):
    """This class creates and writes code for points in gmsh format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, point_id, x, y, z, size):
        """Creates a point."""

        self.point_id = point_id
        self.x = x
        self.y = y
        self.z = z
        self.size = size

#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a point in gmsh format."""
        point_code = 'Point({:d}) = {{{:.9f}, {:.9f}, {:.9f}, {:.9f}}};'.format(
            self.point_id, self.x, self.y, self.z, self.size)


        return point_code + '\n'
#
#-----------------------------------------------------------------------
# END class gmsPoint
#-----------------------------------------------------------------------
#

class gmshLine(object):
    """This class creates and writes code for lines in gmsh format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, line_id, points_ids, linetype):
        """Creates a line with the given points."""

        self.line_id = line_id
        self.ids = points_ids
        self.linetype = linetype
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a line in gmsh format."""

        strids = ', '.join(map(str, self.ids))
        if self.linetype == 'line':
            line_code = 'Line({:d}) = {{{}}};'.format(self.line_id, strids)
        elif self.linetype == 'circle':
            line_code = 'Circle({:d}) = {{{}}};'.format(self.line_id, strids)


        return line_code + '\n'
#
#-----------------------------------------------------------------------
# END class gmshLine
#-----------------------------------------------------------------------
#

class gmshLineLoop(object):
    """This class creates and writes code for line loops in gmsh format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, lineloop_id, lines_ids):
        """Creates a line loop with the given lines."""

        self.lineloop_id = lineloop_id
        self.ids = lines_ids
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a line loop in gmsh format."""

        strids = ', '.join(map(str, self.ids))
        lineloop_code = 'Line Loop({:d}) = {{{}}};'.format(
            self.lineloop_id, strids)

        return lineloop_code + '\n'

#
#-----------------------------------------------------------------------
# END class gmshLineLoop
#-----------------------------------------------------------------------
#

class gmshPlaneSurface(object):
    """This class creates and writes code for plane surfaces in gmsh format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, planesurface_id, lineloops_ids):
        """Creates a plane surface with the given line loops."""

        self.planesurface_id = planesurface_id
        self.ids = []
        self.ids.append(lineloops_ids)

#
#-----------------------------------------------------------------------
#
    def add_lineloop(self, lineloops_ids):
        """Adds a line loop to the physical surface"""
        self.ids.append(lineloops_ids)
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a plane surface in gmsh format."""

        strids = ', '.join(map(str, self.ids))
        planesurface_code = 'Plane Surface({:d}) = {{{}}};'.format(
            self.planesurface_id, strids)

        return planesurface_code + '\n'
#
#-----------------------------------------------------------------------
# END class gmshPlaneSurface
#-----------------------------------------------------------------------
#
class gmshPhysical(object):
    """This class creates and writes code for physical
           surfaces in gmsh format."""
#
#-----------------------------------------------------------------------
#
    def __init__(self, physical_id, name, lineloops_ids, phystype):
        """Creates a physical surface for the given lineloops"""

        self.physical_id = physical_id
        self.name = name
        self.phystype = phystype #surf,  vol
        self.ids = []
        self.ids.extend(lineloops_ids)
#
#-----------------------------------------------------------------------
#
    def add_lineloop(self, lineloops_ids):
        """Adds line loops to the physical surface"""

        self.ids.extend(lineloops_ids)
#
#-----------------------------------------------------------------------
#
    def code(self):
        """Returns the code for a physical surface in gmsh format."""
        from string import Template
        outs = ''
        out = Template('out[$n]')

        for i in self.ids:
            outs = outs + out.substitute(n=i) + ','

        outs = outs[:-1] #removes last comma

        if self.phystype == 'surf':

            physical_code = 'Physical Surface("{:s}") = {{{}}};'.format(
                self.name, outs)

        elif self.phystype == 'vol':

            physical_code = 'Physical Volume("{:s}") = {{{}}};'.format( \
                self.name, outs)

        return physical_code + '\n'
#
#-----------------------------------------------------------------------
# END class gmshPhysical
#-----------------------------------------------------------------------
#
