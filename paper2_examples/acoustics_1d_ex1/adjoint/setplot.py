
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
    
    # Reversing time in adjoint output
    setadjoint()

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()  # clear any old figures,axes,items data
    plotdata.format = 'binary'      # 'ascii', 'binary', 'netcdf'

    def fix_plot(current_data):
        from pylab import plot
        from pylab import xticks,yticks,xlabel,ylabel,savefig,ylim,title
        t = current_data.t
        plot([0., 0.], [-1000., 1000.], 'k--')
        title('Adjoint at t = %5.3f seconds' % t, fontsize=26)
        yticks(fontsize=23)
        xticks(fontsize=23)

    # Figure for q[0]
    plotfigure = plotdata.new_plotfigure(name='Adjoint', figno=1)
    plotfigure.kwargs = {'figsize': (10,3.5)}
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-12,12]
    plotaxes.ylimits = [-0.5,4.3]
    plotaxes.title = 'Adjoint'
    plotaxes.afteraxes = fix_plot

    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 0
    plotitem.amr_color = 'b'
    plotitem.amr_plotstyle = 'o'
    plotitem.amr_kwargs = [{'linewidth':5}]
    plotitem.outdir = '../../adjoint/_outputReversed'

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
    
    files = glob.glob(outdir+'/fort.b0*')
    n = len(files)
    
    # Find the final time.
    fname = files[n-1]
    fname = fname.replace('b','t')
    f = open(fname,'r')
    print(f)
    tfinal,meqn,npatches,maux,num_dim = io.ascii.read_t(n-1,path=outdir)
    
    for k in range(n):
        # Creating new files
        fname = files[k]
        newname = outdir2 + '/fort.b%s' % str(n-k-1).zfill(4)
        cmd = 'cp %s %s' % (fname,newname)
        os.system(cmd)
        
        fname = fname.replace('b','q')
        newname = newname.replace('b','q')
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
        f.write('%5i                  meqn\n' % meqn)
        f.write('%5i                  ngrids\n' % npatches)
        f.write('%5i                  naux\n' % maux)
        f.write('%5i                  ndim\n' % num_dim)
        #f.write('%5i                  nghost\n' % nghost)
        f.close()
# end of function setadjoint
# ----------------------



    
