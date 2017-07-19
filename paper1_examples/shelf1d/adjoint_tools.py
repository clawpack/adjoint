
from clawpack.visclaw.data import ClawPlotData
import numpy as np
import pylab


def read_data(outdir="_output", adjoint=False):
    
    from numpy import loadtxt
    fname = outdir + '/fort.H'
    B = loadtxt(fname)
    print "Loaded B"
    
    pd = ClawPlotData()
    pd.outdir = outdir

    times = []
    qxt = []
    for frameno in range(5001):
        try:
            frame = pd.getframe(frameno)
        except:
            break
        q = frame.state.q
        t = frame.state.t
        q[0,:] = B + q[0,:]
        qxt.append(q)
        times.append(t)
    
    x = frame.state.patch.x.centers
    x = x
    X,T = np.meshgrid(x,times)
    qxt = np.array(qxt)
    if adjoint:
        qxt = np.flipud(qxt)  # reverse t for adjoint
    return X,T,qxt

