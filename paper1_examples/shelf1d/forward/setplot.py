
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

    from numpy import loadtxt
    fname = plotdata.outdir + '/fort.H'
    B = loadtxt(fname)
    print "Loaded B"

    plotdata.clearfigures()  # clear any old figures,axes,items data

    def add_dashes(current_data):
        from pylab import ylim,plot
        plot([-50000,-50000], [-1,1],'k--')

    
    # Figure for eta
    plotfigure = plotdata.new_plotfigure(name='eta', figno=2)
    plotfigure.kwargs = {'figsize':(10,3.5)}

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    def fixfig(current_data):
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        add_dashes(current_data)
        xticks([-350000,-250000,-150000, -50000],['350','250','150','50','0'],\
               fontsize=23)
        yticks([-0.4,-0.2,0.0, 0.2, 0.4],['-0.4','-0.2','0.0','0.2','0.4'],\
               fontsize=23)
        ylabel('Meters', fontsize=23)
        title('Surface at t = %i seconds' % int(t), fontsize=26)

    plotaxes.afteraxes = fixfig
    plotaxes.ylimits = [-0.4, 0.5]
    plotaxes.title = 'Surface'

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d')
    def surface(current_data):
        eta = B + current_data.q[0,:]
        return eta
    plotitem.plot_var = surface
    plotitem.plotstyle = '-'
    plotitem.color = 'b'
    plotitem.kwargs = {'linewidth':2}

    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via clawpack.visclaw.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = [2,3]            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'   # pointer for top of index
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
