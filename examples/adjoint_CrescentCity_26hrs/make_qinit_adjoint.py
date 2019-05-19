"""
    Download topo and dtopo files needed for this example.
    
    Call functions with makeplots==True to create plots of topo, slip, and dtopo.
"""

from __future__ import print_function
import os,sys
import clawpack.clawutil.data
from clawpack.geoclaw import topotools
from numpy import *


# Center of Gaussian for adjoint initial conditions
xcenter = -124.1839 - 15/60.  # shift offshore
radius = 1.0e0
ycenter =41.74512e0   

# Gaussian width parameter in exp(-(r/beta)**2), where r is in meters
beta = 20.e3


def makeqinit():
    """
        Create qinit data file
    """
    
    nxpoints = 201
    nypoints = 201
    
    xlower = xcenter - 1.5
    xupper = xcenter + 1.5
    ylower = ycenter - 1.5
    yupper = ycenter + 1.5
    
    outfile= "hump.xyz"     
    topotools.topo1writer(outfile,qinit,xlower,xupper,ylower,yupper,nxpoints,nypoints)

def qinit(x,y):
    from numpy import where
    from clawpack.geoclaw.util import haversine
    r = haversine(x,y,xcenter,ycenter)
    z = 0.1*exp(-(r/beta)**2)
    return z

if __name__=='__main__':
    makeqinit()
