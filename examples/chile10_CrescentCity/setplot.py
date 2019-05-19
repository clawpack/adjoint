
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

from clawpack.geoclaw import topotools
from six.moves import range

#--------------------------
def setplot(plotdata=None):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    from clawpack.visclaw import colormaps, geoplot
    from numpy import linspace

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()


    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'binary'


    # To plot gauge locations on pcolor or contour plot, use this as
    # an afteraxis function:

    def addgauges(current_data):
        from clawpack.visclaw import gaugetools
        gaugetools.plot_gauge_locations(current_data.plotdata, \
             gaugenos='all', format_string='ko', add_labels=True)
    

    def title_hours(current_data):
        from pylab import title, mod
        t = current_data.t
        hours = int(t/3600.)
        tmin = mod(t,3600.)
        min = int(tmin/60.)
        tsec = mod(tmin,60.)
        sec = int(mod(tmin,60.))
        if t < 120:
            timestr = '%s seconds' % t
        else:
            timestr = '%s:%s:%s' % (hours,str(min).zfill(2),str(sec).zfill(2))
        title('%s after earthquake' % timestr)


    #-----------------------------------------
    # Figure for surface
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=0)
    plotfigure.kwargs = {'figsize':(8,5)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True

    def fixup(current_data):
        import pylab
        addgauges(current_data)
        t = current_data.t
        t = t / 3600.  # hours
        pylab.title('Surface at %4.2f hours' % t, fontsize=20)
        pylab.grid(True)
    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = colormaps.red_white_blue #geoplot.tsunami_colormap
    plotitem.pcolor_cmin = -0.03
    plotitem.pcolor_cmax = 0.03
    plotitem.add_colorbar = False
    plotitem.colorbar_shrink = 0.5
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    plotaxes.xlimits = [-240,-66]
    plotaxes.ylimits = [-47,65]

    #-----------------------------------------
    # Figure for adjoint
    #-----------------------------------------

    # Set up for axes in this figure:
    plotfigure = plotdata.new_plotfigure(name='Adjoint ', figno=20)
    plotfigure.kwargs = {'figsize': (8,5)}
    plotaxes = plotfigure.new_plotaxes('adjoint')
    plotaxes.scaled = True
    plotaxes.title = 'Adjoint flag'

    def fixup(current_data):
        addgauges(current_data)

    plotaxes.afteraxes = fixup


    adj_flag_tol = 0.000001
    def masked_inner_product(current_data):
        from numpy import ma
        q = current_data.q
        soln = ma.masked_where(q[4,:,:] < adj_flag_tol, q[4,:,:])
        return soln
    def masked_regions(current_data):
        from numpy import ma
        q = current_data.q
        soln = ma.masked_where(q[4,:,:] < 1e9, q[4,:,:])
        return soln

    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 4 #masked_inner_product
    plotitem.pcolor_cmap = colormaps.white_red
    plotitem.pcolor_cmin = adj_flag_tol
    plotitem.pcolor_cmax = 100*adj_flag_tol
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0]
    plotitem.amr_data_show = [1,1,0,0,0,0,0,0,0]
    plotitem.patchedges_show = 0

    #plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = masked_regions
    #plotitem.pcolor_cmap = colormaps.white_blue
    #plotitem.pcolor_cmin = 9e9
    #plotitem.pcolor_cmax = 1.1e10
    #plotitem.add_colorbar = False
    #plotitem.amr_celledges_show = [0]
    #plotitem.amr_data_show = [1,1,0,0]
    #plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    plotaxes.xlimits = [-240,-66]
    plotaxes.ylimits = [-47,65]

    #-----------------------------------------
    # Figure for levels
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Grid patches', figno=10)
    plotfigure.kwargs = {'figsize': (8,5)}
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Grid patches'
    plotaxes.scaled = True
    def aa_patches(current_data):
        from pylab import ticklabel_format, xticks, gca, cos, pi, yticks
        ticklabel_format(format='plain',useOffset=False)
        xticks([180, 200, 220, 240], rotation=20, fontsize = 28)
        yticks(fontsize = 28)
        a = gca()
        a.set_aspect(1./cos(41.75*pi/180.))

    def fixup(current_data):
        import pylab
        addgauges(current_data)
        t = current_data.t
        t = t / 3600.  # hours
        pylab.title('Grid patches at %4.2f hours' % t, fontsize=20)
        pylab.grid(True)
    plotaxes.afteraxes = fixup
    
    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_patch')
    plotitem.amr_patch_bgcolor = [[1,1,1], [0.8,0.8,0.8], [0.8,1,0.8], [1,.7,.7],[0.6,0.6,1]]
    plotitem.amr_patchedges_color = ['k','k','g','r','b']
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0,1,1,1,1]
    
    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0]
    plotaxes.xlimits = [-240,-66]
    plotaxes.ylimits = [-47,65]

    #-----------------------------------------
    # Zoom
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Crescent City Agrid', figno=1)
    #plotfigure.show = False
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = -0.1
    plotitem.pcolor_cmax = 0.1
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    #plotaxes.xlimits = [-161.,-154.0333]
    #plotaxes.ylimits = [18.0317,22.9983]
    plotaxes.xlimits = [-126.995,-123.535]
    plotaxes.ylimits = [40.515,44.495]

    #-----------------------------------------
    # Zoom2
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Crescent City Zoom', figno=2)
    #plotfigure.show = False
    plotfigure.show = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes('pcolor')
    plotaxes.title = 'Surface'
    plotaxes.scaled = True
    plotaxes.afteraxes = fixup

    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    #plotitem.plot_var = geoplot.surface
    plotitem.plot_var = geoplot.surface_or_depth
    plotitem.pcolor_cmap = geoplot.tsunami_colormap
    plotitem.pcolor_cmin = -0.1
    plotitem.pcolor_cmax = 0.1
    plotitem.add_colorbar = True
    plotitem.colorbar_shrink = 0.5
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0

    # Land
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = geoplot.land
    plotitem.pcolor_cmap = geoplot.land_colors
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 100.0
    plotitem.add_colorbar = False
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.patchedges_show = 0
    plotaxes.xlimits = [-124.2345,-124.1434]
    plotaxes.ylimits = [41.7168,41.7829]

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Surface at gauges', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.title = 'Surface'

    # Plot surface as blue curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 3
    plotitem.plotstyle = 'b-'

    # Plot topo as green curve:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = False

    def gaugetopo(current_data):
        q = current_data.q
        h = q[0,:]
        eta = q[3,:]
        topo = eta - h
        return topo
        
    plotitem.plot_var = gaugetopo
    plotitem.plotstyle = 'g-'

    def add_zeroline(current_data):
        from pylab import plot, legend, xticks, floor, axis, xlabel, \
                xlim, ylim
        t = current_data.t 
        gaugeno = current_data.gaugeno
        plot(t, 0*t, 'k')
        n = int(floor(t.max()/3600.) + 2)
        xticks([3600*i for i in range(n)], ['%i' % i for i in range(n)])
        xlabel('time (hours)')
        xlim(14.5*3600,26.0*3600)
        ylim(-1.5,1.5)

    plotaxes.afteraxes = add_zeroline



    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_gaugenos = 'all'          # list of gauges to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.parallel = True                 # make multiple frame png's at once

    return plotdata

