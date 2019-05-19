
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

from __future__ import absolute_import
from __future__ import print_function

#--------------------------
def setplot(plotdata=None):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of clawpack.visclaw.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 


    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()  # clear any old figures,axes,items data

    def fix_plot(current_data):
        from pylab import plot
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        plot([0., 0.], [-1000., 1000.], 'k--')
        title('Pressure at t = %5.3f seconds' % t, fontsize=26)
        yticks(fontsize=23)
        xticks(fontsize=23)

    def fix_plot_innerprod(current_data):
        from pylab import plot
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        plot([0., 0.], [-1000., 1000.], 'k--')
        title('Pressure at t = %5.3f seconds' % t, fontsize=26)
        yticks(fontsize=23)
        xticks(fontsize=23)


    # Figure for q[0]
    plotfigure = plotdata.new_plotfigure(name='Pressure', figno=1)
    plotfigure.kwargs = {'figsize': (10,3.5)}
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-12,12]
    plotaxes.ylimits = [-1.1,1.1]
    plotaxes.title = 'Pressure'
    plotaxes.afteraxes = fix_plot

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.amr_color = 'b'
    plotitem.amr_plotstyle = 'o'
    plotitem.amr_kwargs = [{'linewidth':2}]
    plotitem.amr_kwargs = [{'markersize':4}]

    # Figure for inner product, q[2]
    
    plotfigure = plotdata.new_plotfigure(name='Inner Product', figno=10)
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = 'auto'
    #plotaxes.ylimits = [-.5,1.1]      # use when taking inner product with forward solution
    plotaxes.ylimits = [0,0.02]    # use when taking inner product with Richardson error
    plotaxes.title = 'Inner Product'
    plotaxes.afteraxes = fix_plot_innerprod
    
    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    plotitem.plot_var = 2
    plotitem.amr_color = 'b'
    plotitem.amr_plotstyle = 'o'
    plotitem.amr_kwargs = [{'linewidth':2}]
    plotitem.amr_data_show = [1,1,1,0]
    plotitem.show = True       # show on plot?

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
