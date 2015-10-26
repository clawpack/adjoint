"""
    Comparing refinement with adjoint-flagging vs refinement using
    pressure-flagging, which is the current default.
"""

import os

currentdir = os.getcwd()
adjointdir = currentdir + '/adjoint'

os.chdir(adjointdir)
os.system('make new')
os.system('make .plots')

# Modify the setrun.py file to use the correct tolerance
os.chdir(currentdir)
f = open('setrun.py').read()
f = f.replace("    amrdata.flag2refine_tol = 0.02 # tolerance used in this routine\n", "    amrdata.flag2refine_tol = 0.1 # tolerance used in this routine\n")
open('setrun.py','w').write(f)

# Run example using pressure flagging
os.system('make new -f Makefile_pflag')
os.system('make .plots -f Makefile_pflag')

# Rename output folder
os.system('rm -r _output_pflag')
os.system('mv _output _output_pflag')
os.system('rm -r _plots_pflag')
os.system('mv _plots _plots_pflag')

# Modify the setrun.py file to use the correct tolerance
os.chdir(currentdir)
f = open('setrun.py').read()
f = f.replace("    amrdata.flag2refine_tol = 0.1 # tolerance used in this routine\n", "    amrdata.flag2refine_tol = 0.02 # tolerance used in this routine\n")
open('setrun.py','w').write(f)

# Uncomment code to plot divided differences output at gauge
os.chdir(currentdir)
f = open('setplot.py').read()
f = f.replace("#plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    #plotitem.plot_var = 0\n    #plotitem.plotstyle = 'rs'\n    #plotitem.outdir = '../_output_pflag'", "plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    plotitem.plot_var = 0\n    plotitem.plotstyle = 'rs'\n    plotitem.outdir = '../_output_pflag'")
open('setplot.py','w').write(f)

# Run example using adjoint method
os.chdir(currentdir)
os.system('make new')
os.system('make .plots')

# Return setplots.py to default (not comparing gauge results with pressure flagging output)
os.chdir(currentdir)
f = open('setplot.py').read()
f = f.replace("plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    plotitem.plot_var = 0\n    plotitem.plotstyle = 'rs'\n    plotitem.outdir = '../_output_pflag'", "#plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    #plotitem.plot_var = 0\n    #plotitem.plotstyle = 'rs'\n    #plotitem.outdir = '../_output_pflag'")
open('setplot.py','w').write(f)

print 'Finished running example comparing adjoint refinement with divided differences refinement'