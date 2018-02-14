
def read_data(xpts, outdir="_output", adjoint=False):

    from clawpack.visclaw.data import ClawPlotData
    from numpy import ma
    import numpy as np
    
    pd = ClawPlotData()
    pd.outdir = outdir
    if adjoint:
        pd.format = 'binary'
    
    times = []
    qxt = []
    vxt = []
    levs = []

    for frameno in range(5001):
        try:
            frame = pd.getframe(frameno)
        except:
            break
        t = frame.state.t
        times.append(t)
        q_pts = ma.masked_array(np.zeros(xpts.shape),mask=True)
        v_pts = ma.masked_array(np.zeros(xpts.shape),mask=True)
        level_pts = ma.masked_array(np.zeros(xpts.shape),mask=True)

        states = frame.states
        # loop over all patches
        for state in states:
            q = state.q
            patch = state.patch
            xlower = patch.dimensions[0].lower
            xupper = patch.dimensions[0].upper
            dx = patch.delta[0]
        
            meqn,mx = q.shape
            pts_in_patch = np.logical_and(xpts >= xlower, xpts <= xupper)

            level_pts[pts_in_patch] = patch.level

            q_in_patch = []
            v_in_patch = []
            for xp in xpts[pts_in_patch]:
                i = min(int(np.floor((xp - xlower)/dx)), mx-1)
                q_in_patch.append(q[0,i])
                v_in_patch.append(q[1,i])
            
            q_pts[pts_in_patch] = q_in_patch
            v_pts[pts_in_patch] = v_in_patch
        
        qxt.append(q_pts)
        vxt.append(v_pts)
        levs.append(level_pts)

    X,T = np.meshgrid(xpts,times)
    qxt = np.array(qxt)
    vxt = np.array(vxt)
    levs = np.array(levs)
    if adjoint:
        qxt = np.flipud(qxt)  # reverse t for adjoint
        vxt = np.flipud(vxt)  # reverse t for adjoint
    return X,T,qxt,vxt,levs
