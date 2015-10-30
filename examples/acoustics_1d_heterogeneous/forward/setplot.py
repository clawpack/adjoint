def setplot(plotdata):
    
    # Reversing time in adjoint output
    setadjoint()
    
    plotdata.clearfigures()

    # Tuples of (variable name, variable number)
    figdata = [('Pressure', 0),
               ('Velocity', 1)]

    # Draw a vertical dashed line at the interface
    # between different media
    def draw_interface(current_data):
        import pylab
        pylab.plot([0., 0.], [-1000., 1000.], 'k--')
    
    # Formatting title
    def format(current_data, var, adjoint):
        import pylab
        size = 28
        t = current_data.t
        timestr = float(t)
        
        if (var == 0):
            titlestr = 'Forward Pressure'
        else:
            titlestr = 'Velocity at time %s' % timestr
        if(adjoint):
            titlestr = 'Adjoint Pressure'
            pylab.tick_params(axis='y', labelleft='off')
        
        pylab.title(titlestr, fontsize=size)
        pylab.xticks(fontsize=size)
        pylab.yticks(fontsize=size)
        pylab.xticks([-4, -2, 0, 2], fontsize=size)
    
    # After axis function for pressure
    def aa_pressure(current_data):
        draw_interface(current_data)
        format(current_data, 0, False)

    # After axis function for velocity
    def aa_velocity(current_data):
        draw_interface(current_data)
        format(current_data, 1, False)
    
    # After axis function for adjoint pressure
    def aa_pressure_adjoint(current_data):
        draw_interface(current_data)
        format(current_data, 0, True)
    
    # After axis function for adjoint velocity
    def aa_velocity_adjoint(current_data):
        draw_interface(current_data)
        format(current_data, 1, True)

    for varname, varid in figdata:
        plotfigure = plotdata.new_plotfigure(name=varname, figno=varid)
        plotfigure.kwargs = {'figsize': (11,5)}

        plotaxes = plotfigure.new_plotaxes()
        plotaxes.axescmd = 'axes([0.1,0.1,0.4,0.8])'
        plotaxes.xlimits = [-5., 3.]
        plotaxes.ylimits = [-0.5, 1.5]    # Good for both vars because of near-unit impedance
        if (varid == 0):
            plotaxes.afteraxes = aa_pressure
        else:
            plotaxes.afteraxes = aa_velocity

        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = varid
        plotitem.color = 'b'
    
        # Adding adjoint plot
        plotaxes = plotfigure.new_plotaxes()
        plotaxes.axescmd = 'axes([0.56,0.1,0.4,0.8])'
        plotaxes.xlimits = [-5., 3.]
        plotaxes.ylimits = [-0.5, 1.5]    # Good for both vars because of near-unit impedance
        if (varid == 0):
            plotaxes.afteraxes = aa_pressure_adjoint
        else:
            plotaxes.afteraxes = aa_velocity_adjoint
        
        import os
        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = varid
        plotitem.color = 'b'
        plotitem.outdir = os.path.join(os.getcwd(), '../adjoint/_outputReversed')

    plotdata.printfigs = True          # Whether to output figures
    plotdata.print_format = 'png'      # What type of output format
    plotdata.print_framenos = 'all'    # Which frames to output
    plotdata.print_fignos = 'all'      # Which figures to print
    plotdata.html = True               # Whether to create HTML files
    plotdata.latex = False             # Whether to make LaTeX output

    return plotdata

#-------------------
def setadjoint():
    #-------------------
    
    """
        Reverse order of adjoint images, for plotting
        adjacent to forward plots.
    """
    
    import os,sys,glob
    from clawpack.pyclaw import io
    
    outdir = '../adjoint/_output'
    outdir2 = '../adjoint/_outputReversed'
    
    os.system('mkdir -p %s' % outdir2)
    
    files = glob.glob(outdir+'/fort.q0*')
    files.sort()
    n = len(files)
    
    # Find the final time.
    fname = files[n-1]
    fname = fname.replace('q','t')
    f = open(fname,'r')
    tfinal,meqn,npatches,maux,num_dim = io.ascii.read_t(n-1,path=outdir)
    
    for k in range(n):
        # Creating new files
        fname = files[k]
        newname = outdir2 + '/fort.q%s' % str(n-k-1).zfill(4)
        cmd = 'cp %s %s' % (fname,newname)
        os.system(cmd)
        
        fname = fname.replace('q','t')
        newname = newname.replace('q','t')
        cmd = 'cp %s %s' % (fname,newname)
        os.system(cmd)
        
        # Reversing time
        f = open(newname,'r+')
        frameno = n-k-1
        t,meqn,npatches,maux,num_dim = io.ascii.read_t(frameno,path=outdir2)
        t = tfinal - t
        
        # Writting new time out to file
        f.write('%18.8e     time\n' % t)
        f.write('%5i                  num_eqn\n' % meqn)
        f.write('%5i                  nstates\n' % npatches)
        f.write('%5i                  num_aux\n' % maux)
        f.write('%5i                  num_dim\n' % num_dim)
        f.close()
# end of function setadjoint
# ----------------------

