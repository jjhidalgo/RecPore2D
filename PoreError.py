"""Exception managing for RegPore2D."""

class PoreError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self):
        """ Does nothing"""
        Exception.__init__(self)

class ErrorPacking(PoreError):
    """Exception raised for errors in the packing.

    The only allowed packings are:
        tri -- triangular
        sqr  -- square
        etri -- elongated triangular
    """
    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        print ("Wrong packing!")

class ErrorNx(PoreError):
    """Exception raised for nx!
    It is negative or an even number with tri and etri packings."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Number of grains in x direction too small, negative,"
        msg = msg + "or even with tri and etri packings!"
        print (msg)

class ErrorNy(PoreError):
    """Exception raised for ny<1  or nx*radius>1.0!"""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        print ("Number of grains in y direction too small or negative!")

class ErrorRadius(PoreError):
    """Exception raised for grain radius. Radius <1e-9"""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        print ("Grain radius too small or negative!")

class ErrorThroatNegative(PoreError):
    """Exception raised for pore throat. Pore throat is negative"""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        print ("Pore throat negative! Check number of grains in y and radius.")

class ErrorNotPorousMedium(PoreError):
    """Exception when an variable is not an instance of RegPore2D."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "A porous medium (instance of RegPore2D"
        msg = msg + " is needed for this operation."
        print (msg)

class ErrorRmin(PoreError):
    """Exception when minimun grain radius is negative, zero,
       or greater than the maximum radius."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Minimun grain radius too small, zero or greater than maximum radius."
        print (msg)

class ErrorRmax(PoreError):
    """Exception when maximum grain radius is negative, zero,
       or lower than minimum radius."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Maximun grain radius too small, zero or lower than minimum radius."
        print (msg)

class ErrorLx(PoreError):
    """Exception when horizontal lenght is zero or negative."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Lx too small or negative."
        print (msg)

class ErrorLy(PoreError):
    """Exception when vertical lenght is zero or negative."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Ly too small or negative."
        print (msg)

class ErrorPorosity(PoreError):
    """Exception when porosity is zero, negative, or greater than 1."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Porosity  is negative, zero, or greater than one."
        print (msg)

class ErrorNtriesMax(PoreError):
    """Exception when maximum number of attempts to add a new grain is zero
       or negative."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Number of tries must be greater than zero."
        print (msg)

class ErrorNgrainsMax(PoreError):
    """Exception when maximum allowed number of grains is negative or zero."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "The maximum number of grains must be greater than zero."
        print (msg)

class ErrorNBlocks(PoreError):
    """Exception when the number of blocks for PySnnapy is zero or negative
       in some direction."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "The number of blocks in all directions must be greater than zero."
        print (msg)

class ErrorSize(PoreError):
    """Exception when the mesh size is zero or negative."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Mesh size must be greater than zero."
        print (msg)

class ErrorXoffset(PoreError):
    """Exception when the x offset is wrong."""

    def __init__(self):
        """Just prints the error message"""
        PoreError.__init__(self)
        msg = "Something is wrong with the x offset."
        print (msg)


