def setplot(plotdata):
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
    def format_title(current_data, var, adjoint):
        from pylab import title
        t = current_data.t
        t = 20.0 - t 
        timestr = float(t)
        
        if (var == 0):
            titlestr = 'Pressure at time %s' % timestr
        else:
            titlestr = 'Velocity at time %s' % timestr
        if(adjoint):
            titlestr = 'Adjoint ' + titlestr
    
        title(titlestr)

    # Afteraxis function for pressure plots
    def aa_pressure(current_data):
        draw_interface(current_data)
        format_title(current_data, 0, False)
    
    # Afteraxis function for velocity plots
    def aa_velocity(current_data):
        draw_interface(current_data)
        format_title(current_data, 1, False)

    for varname, varid in figdata:
        plotfigure = plotdata.new_plotfigure(name=varname, figno=varid)

        plotaxes = plotfigure.new_plotaxes()
        plotaxes.xlimits = [-5., 3.]
        plotaxes.ylimits = [-0.5, 1.5]    # Good for both vars because of near-unit impedance
        if (varid == 0):
            plotaxes.afteraxes = aa_pressure
        else:
            plotaxes.afteraxes = aa_velocity

        plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
        plotitem.plot_var = varid
        plotitem.color = 'b'

    plotdata.printfigs = True          # Whether to output figures
    plotdata.print_format = 'png'      # What type of output format
    plotdata.print_framenos = 'all'    # Which frames to output
    plotdata.print_fignos = 'all'      # Which figures to print
    plotdata.html = True               # Whether to create HTML files
    plotdata.latex = False             # Whether to make LaTeX output

    return plotdata

