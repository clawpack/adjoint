
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
"""

#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 

    from clawpack.visclaw import colormaps

    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'binary'      # 'ascii', 'binary', 'netcdf'
    

    # Figure for pressure
    # -------------------

    plotfigure = plotdata.new_plotfigure(name='Pressure', figno=0)
    plotfigure.kwargs = {'figsize': (5.5,4)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-8,8]
    plotaxes.ylimits = [-1,11]
    plotaxes.title = 'Pressure'
    plotaxes.scaled = True      # so aspect ratio is 1
    plotaxes.afteraxes = fixup

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 0
    plotitem.pcolor_cmap = colormaps.blue_white_red
    plotitem.add_colorbar = False
    plotitem.show = True       # show on plot?
    plotitem.pcolor_cmin = -0.3
    plotitem.pcolor_cmax = 0.3
    plotitem.amr_patchedges_show = [0,0,0,0,0]
    plotitem.amr_celledges_show = [0,0,0,0,0]
    
    #-----------------------------------------
    # Figure for innerproduct
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Inner Product', figno=1)
    plotfigure.kwargs = {'figsize': (5.5,4)}
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Inner Product'
    plotaxes.xlimits = [-8,8]
    plotaxes.ylimits = [-1,11]
    plotaxes.title = 'Inner Product'
    plotaxes.scaled = True      # so aspect ratio is 1
    plotaxes.afteraxes = fixup_innerprod
    
    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = plot_innerprod
    plotitem.pcolor_cmap = colormaps.white_red
    plotitem.add_colorbar = False
    plotitem.show = True       # show on plot?
    plotitem.pcolor_cmin = 0.01     # use when plotting inner product with q
    #plotitem.pcolor_cmin = 0.0      # use when plotting inner product with error
    plotitem.pcolor_cmax = 0.12    # use when plotting inner product with q
    #plotitem.pcolor_cmax = 0.005    # use when plotting inner product with error
    plotitem.amr_patchedges_show = [0,0,0]
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_data_show = [1,1,1,1,0]
    
    #-----------------------------------------
    # Figure for levels
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='Grid patches', figno=10)
    plotfigure.kwargs = {'figsize': (5.5,4)}
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-8,8]
    plotaxes.ylimits = [-1,11]
    plotaxes.title = 'Grid patches'
    plotaxes.scaled = True
    plotaxes.afteraxes = fixup
    
    # Water
    plotitem = plotaxes.new_plotitem(plot_type='2d_patch')
    plotitem.amr_patch_bgcolor = [[1,1,1], [0.8,0.8,0.8], [0.8,1,0.8], [1,.7,.7],[0.6,0.6,1]]
    plotitem.amr_patchedges_color = ['k','k','g','r','b']
    plotitem.amr_celledges_show = [0]
    plotitem.amr_patchedges_show = [0,1,1,1,1]

    #-----------------------------------------
    # Figures for gauges
    #-----------------------------------------
    plotfigure = plotdata.new_plotfigure(name='q', figno=300, \
                    type='each_gauge')
    plotfigure.clf_each_gauge = True

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    plotaxes.ylimits = 'auto'
    plotaxes.xlimits = [1,3]
    plotaxes.ylimits = [-0.4,0.5]
    plotaxes.title = 'Pressure'
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.plotstyle = 'b-'
    plotitem.kwargs = {'linewidth': 3}
    plotaxes.afteraxes = fixup_gauge

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.html_movie = 'JSAnimation'      # new style, or "4.x" for old style
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

def plot_innerprod(current_data):
    return current_data.aux[2,:,:]

# Afteraxis functions:

def addgauges(current_data):
    from clawpack.visclaw import gaugetools
    gaugetools.plot_gauge_locations(current_data.plotdata, \
                gaugenos='all', format_string='ko', add_labels=True, fontsize=14)

def fixup(current_data):
    import pylab
    from pylab import plot
    size = 28
    plot_rectangle(current_data)
    # Uncomment this line if you want to generate plots without a title for the paper
    #pylab.title(' ')
    pylab.xticks([-8, -4, 0, 4, 8], fontsize=size)
    pylab.yticks([0, 5, 10], fontsize=size)
    plot([0., 0.], [-1000., 1000.], 'k--')

def fixup_innerprod(current_data):
    import pylab
    from pylab import plot
    size = 28
    plot_rectangle(current_data)
    pylab.xticks([-8, -4, 0, 4, 8], fontsize=size)
    pylab.yticks([0, 5, 10], fontsize=size)
    plot([0., 0.], [-1000., 1000.], 'k--')

def plot_rectangle(current_data):
    from clawpack.visclaw.plottools import plotbox
    x1 = 3.18; x2 = 3.82; y1 = 0.26; y2 = 0.74
    xy = [x1, x2, y1, y2]
    plotbox(xy, kwargs={'color': 'k', 'linewidth': 2})

def fixup_gauge(current_data):
    import pylab
    size = 34
    pylab.title('Pressure at Gauge 0', fontsize=size)
    pylab.xticks([1.0, 1.5, 2.0, 2.5, 3.0], fontsize=size)
    pylab.yticks([-0.3, -0.1, 0.1, 0.3, 0.5], fontsize=size)
