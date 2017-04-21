"""2D rectangular porous medium generation"""

import numpy as np

class Grain(object):
    """A grain."""

    def __init__(self, rmin=0.1, rmax=0.3, lx=1., ly=1., tolerance=0.02):

        self._x = None
        self._y = None
        self._radius = None
        self._area = None
        self._tolerance = None

        self.x = np.random.uniform(0.0, lx)
        self.y = np.random.uniform(0.0, ly)
        self.radius = np.random.uniform(rmin, rmax)
        #aa = np.exp(np.random.lognormal(1.,1.,1))
        
        self.area = np.pi*self.radius*self.radius
        self.tolerance = tolerance
#
#-----------------------------------------------------------------------
#
    @property
    def x(self):
        """Gets x coordinate of the center"""

        return self._x
#
#-----------------------------------------------------------------------
#
    @x.setter
    def x(self, value):
        """Sets x coordinate of the center."""

        self._x = value
#
#-----------------------------------------------------------------------
#
    @property
    def y(self):
        """Gets y coordinate of the center"""

        return self._y
#
#-----------------------------------------------------------------------
#
    @y.setter
    def y(self, value):
        """Sets x coordinate of the center."""

        self._y = value
#
#-----------------------------------------------------------------------
#
    @property
    def radius(self):
        """Gets y grain radius"""

        return self._radius
#
#-----------------------------------------------------------------------
#
    @radius.setter
    def radius(self, radius):
        """Sets x coordinate of the center."""

        self._radius = radius
#
#-----------------------------------------------------------------------
#
    @property
    def area(self):
        """Gets y grain's area."""

        return self._area
#
#-----------------------------------------------------------------------
#
    @area.setter
    def area(self, area):
        """Sets grain's area."""

        self._area = area
#
#-----------------------------------------------------------------------
#
    @property
    def tolerance(self):
        """Gets tolerance."""

        return self._tolerance
#
#-----------------------------------------------------------------------
#
    @tolerance.setter
    def tolerance(self, value):
        """Sets tolerance."""

        self._tolerance = value
#
#-----------------------------------------------------------------------
#
    def overlap_grains(self, grains):
        """Check if grain overlaps any of the given grains."""

        tolerance = self.tolerance
        if grains:

            xx = np.fromiter((gr.x for gr in grains), dtype='float64')
            yy = np.fromiter((gr.y for gr in grains), dtype='float64')
            rr = np.fromiter((gr.radius for gr in grains), dtype='float64')

            #Distancia entre centros
            center_distance = np.sqrt((self.x - xx)**2. + (self.y - yy)**2.)

            #radii_diff = np.abs(self.radius - rr)
            radii_sum = self.radius + rr + tolerance

            TooFar = all(center_distance > radii_sum)
            # Contained = any(center_distance < radii_diff)
            # SameGrain = any(center_distance > tolerance) and \
            #             any(abs(radii_diff) < tolerance)

            Overlap = not TooFar #or Contained or SameGrain

        else:

            Overlap = False
            
        return Overlap

#
#-----------------------------------------------------------------------
#
    def overlap_rectangle(self, pmin, pmax):
        """Check if grain overlaps a rectangle."""

        tolerance = self._tolerance
        TouchesLeftSide = (self.x - self.radius) < (pmin[0] + tolerance)
        TouchesRightSide = (self.x + self.radius) > (pmax[0] - tolerance)
        TouchesTop = (self.y + self.radius) > (pmax[1] - tolerance)
        TouchesBottom = (self.y - self.radius) < (pmin[1] + tolerance)

        return TouchesLeftSide or TouchesRightSide or TouchesTop or TouchesBottom
#
#-----------------------------------------------------------------------
# END class Grain
#-----------------------------------------------------------------------
#
