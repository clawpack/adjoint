"""
    Comparing refinement with adjoint-flagging vs refinement using
    surface-flagging by running the full code for all three runs.
"""

import os

currentdir = os.getcwd()
adjointdir = currentdir + '/../adjoint'
forwarddir = currentdir + '/..'

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
os.chdir(forwarddir)
os.system('python maketopo.py')

os.chdir(currentdir)
# Running the example using the tol = 0.14
os.system('make new -f Makefile_sflag_hightol')
os.system('make .plots -f Makefile_sflag_hightol')
os.system('rm -f .data')

# Renaming output folders
os.system('rm -r _output_sflag_14')
os.system('mv _output _output_sflag_14')
os.system('rm -r _plots_sflag_14')
os.system('mv _plots _plots_sflag_14')

# Running the example using tol = 0.09
os.system('make new -f Makefile_sflag_lowtol')
os.system('make .plots -f Makefile_sflag_lowtol')
os.system('rm -f .data')

# Renaming output folders
os.system('rm -r _output_sflag_09')
os.system('mv _output _output_sflag_09')
os.system('rm -r _plots_sflag_09')
os.system('mv _plots _plots_sflag_09')

#-------------------------------------------
# Compute solution for forward problem using adjoint-flagging
#-------------------------------------------

os.chdir(currentdir)
os.system('make new -f Makefile_compare')
os.system('make .plots -f Makefile_compare')

print 'Finished running example comparing adjoint refinement with divided differences refinement'
