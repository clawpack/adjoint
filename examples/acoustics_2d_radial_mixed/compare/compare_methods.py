"""
    Comparing refinement with adjoint-flagging vs refinement using
    pressure-flagging, which is the current default.
"""

import os

currentdir = os.getcwd()
adjointdir = currentdir + '/../adjoint'

# Running adjoint problem
os.chdir(adjointdir)
os.system('rm -f .data')
os.system('make new')
os.system('make .plots')

# Run example using pressure flagging
os.chdir(currentdir)
os.system('rm -f .data')
os.system('make new -f Makefile_pflag')
os.system('make .plots -f Makefile_pflag')

# Rename output folders
os.chdir(currentdir)
os.system('rm -r _output_pflag')
os.system('mv _output _output_pflag')
os.system('rm -r _plots_pflag')
os.system('mv _plots _plots_pflag')

# Run example using adjoint method
os.chdir(currentdir)
os.system('rm -f .data')
os.system('make new -f Makefile_compare')
os.system('make .plots -f Makefile_compare')

print 'Finished running example comparing adjoint refinement with divided differences refinement'