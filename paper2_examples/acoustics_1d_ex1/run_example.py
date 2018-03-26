"""
    Running example multiple times to get average timings
"""

import os

#runs = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20']

runs = ['01','02']

flagging = 'adjoint_magnitude'
tol = '1e-2'

currentdir = os.getcwd()
adjointdir = currentdir + '/adjoint'

# Running the adjoint problem
os.chdir(adjointdir)
os.system('rm -f .data')
os.system('make new')
os.system('make .plots > output_' + tol + '.txt')

for run in runs:
    foutdir = currentdir + '/' + flagging + '/' + tol
    if not os.path.exists(foutdir):
        os.makedirs(foutdir)
    
    # Running the forward problem
    os.chdir(currentdir)
    os.system('rm -f .data')
    os.system('make new')
    os.system('make .output > ' + foutdir + '/output_' + run + '.txt')
    
    # Renaming output folders
    ffolder = '/_output_' + run
    #pfolder = '/_plots_' + run

    os.system('rm -r ' + foutdir + ffolder)
    os.system('mv _output '  + foutdir + ffolder)
    #os.system('rm -r ' + poutdir + pfolder)
    #os.system('mv _plots ' + poutdir + pfolder)

print 'Finished running example for tol ' + tol