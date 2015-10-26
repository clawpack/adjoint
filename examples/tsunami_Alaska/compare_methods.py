"""
    Comparing refinement with adjoint-flagging vs refinement using
    surface-flagging by running the full code for all three runs.
"""

import os

currentdir = os.getcwd()
adjointdir = currentdir + '/adjoint'

#-------------------------------------------
# Compute solution for adjoint problem
#-------------------------------------------

os.chdir(adjointdir)
os.system('python maketopo.py')
os.system('make new')
os.system('make .plots')

#-------------------------------------------
# Compute solution for forward problem using surface-flagging
#-------------------------------------------
os.chdir(currentdir)

os.system('make new -f Makefile_sflag')
os.system('python maketopo.py')

for num in range(1,3):
    # Modifying setrun to use the correct tolerance
    f = open('setrun.py').read()
    if num == 1:
        f = f.replace("refinement_data.wave_tolerance = 0.09\n", "refinement_data.wave_tolerance = 0.14\n")
    if num == 2:
        f = f.replace("refinement_data.wave_tolerance = 0.14\n", "refinement_data.wave_tolerance = 0.09\n")
    open('setrun.py','w').write(f)
    
    # Run example
    os.system('make .plots -f Makefile_sflag')

    # Rename output folders
    if num == 1:
        os.system('rm -r _output_sflag_14')
        os.system('mv _output _output_sflag_14')
        os.system('rm -r _plots_sflag_14')
        os.system('mv _plots _plots_sflag_14')
    if num == 2:
        os.system('rm -r _output_sflag_09')
        os.system('mv _output _output_sflag_09')
        os.system('rm -r _plots_sflag_09')
        os.system('mv _plots _plots_sflag_09')

#-------------------------------------------
# Compute solution for forward problem using adjoint-flagging
#-------------------------------------------

# Uncomment code to plot divided differences output at gauge
os.chdir(currentdir)
f = open('setplot.py').read()
f = f.replace("#plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    #plotitem.plot_var = 3\n    #plotitem.plotstyle = 'r-'\n    #plotitem.outdir = '../_output_sflag_14'", "plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    plotitem.plot_var = 3\n    plotitem.plotstyle = 'r-'\n    plotitem.outdir = '../_output_sflag_14'")
f = f.replace("#plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    #plotitem.plot_var = 3\n    #plotitem.plotstyle = 'g-'\n    #plotitem.outdir = '../_output_sflag_09'", "plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    plotitem.plot_var = 3\n    plotitem.plotstyle = 'g-'\n    plotitem.outdir = '../_output_sflag_09'")
open('setplot.py','w').write(f)

# Run example using adjoint method
os.chdir(currentdir)
os.system('make new')
os.system('make .plots')

# Return setplots.py to default (not comparing gauge results with divided differences output)
os.chdir(currentdir)
f = open('setplot.py').read()
f = f.replace("plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    plotitem.plot_var = 3\n    plotitem.plotstyle = 'r-'\n    plotitem.outdir = '../_output_sflag_14'", "#plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    #plotitem.plot_var = 3\n    #plotitem.plotstyle = 'r-'\n    #plotitem.outdir = '../_output_sflag_14'")
f = f.replace("plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    plotitem.plot_var = 3\n    plotitem.plotstyle = 'g-'\n    plotitem.outdir = '../_output_sflag_09'", "#plotitem = plotaxes.new_plotitem(plot_type='1d_plot')\n    #plotitem.plot_var = 3\n    #plotitem.plotstyle = 'g-'\n    #plotitem.outdir = '../_output_sflag_09'")
open('setplot.py','w').write(f)

print 'Finished running example comparing adjoint refinement with divided differences refinement'