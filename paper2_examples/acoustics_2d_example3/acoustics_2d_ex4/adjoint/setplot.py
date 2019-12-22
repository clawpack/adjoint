
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import os

#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
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
    plotaxes.afteraxes = fixup_adjoint

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotitem.plot_var = 0
    plotitem.pcolor_cmap = colormaps.blue_white_red
    plotitem.pcolor_cmin = -0.005
    plotitem.pcolor_cmax = 0.005
    plotitem.add_colorbar = False
    

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

def fixup_adjoint(current_data):
    import pylab
    from pylab import plot
    size = 28
    plot_rectangle(current_data)
    # Uncomment this line if you want to generate plots without a title for the paper
    #pylab.title(' ')
    pylab.xticks([-8, -4, 0, 4, 8], fontsize=size)
    pylab.yticks([0, 5, 10], fontsize=size)
    plot([0., 0.], [-1000., 1000.], 'k--')

def plot_rectangle(current_data):
    from clawpack.visclaw.plottools import plotbox
    x1 = 3.18; x2 = 3.82; y1 = 0.26; y2 = 0.74
    xy = [x1, x2, y1, y2]
    plotbox(xy, kwargs={'color': 'k', 'linewidth': 2})
