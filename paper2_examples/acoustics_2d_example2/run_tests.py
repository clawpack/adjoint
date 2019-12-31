
from pylab import *
import clawpack.pyclaw.gauges as gauges
from scipy.interpolate import interp1d
from clawpack.clawutil import runclaw
import setrun_cases

# number of reps to run for each case for timing:
num_reps = 5

# gauge and time interval for error estimates:
gaugeno=0
t1 = 20.5
t2 = 21.5

# direct output from all runs to the same temp output directory:
outdir = '_output_temp'


# Read in fine grid reference results for estimating errors
# Assumes code was already run with uniform fine grid, via
#    make .output -f Makefile_fine

gauge = gauges.GaugeSolution(gaugeno, '_output_fine')
t = gauge.t
q = gauge.q
p = q[0,:]
j = where(logical_and(t>t1-0.1,t<t2+0.1))[0]
tt = t[j]
pp = p[j]

tunif = linspace(t1,t2,10000)
pfcn = interp1d(tt,pp)
pfine = pfcn(tunif)  # reference value


def run_test(case):
    
    """
    Run num_rep repetitions of a single test case
    and print out mean CPU time and error.
    """
    
    cpu_times = []
    perrs = []
    
    for k in range(num_reps):
        runclaw.runclaw('xamr',outdir=outdir)
        
        timings = open('%s/timing.txt' % outdir).readlines()
        for line in timings:
            if 'Total time:' in line:
                tokens = line.split()
                cpu_time = float(tokens[-1])
                        
        gauge = gauges.GaugeSolution(gaugeno, outdir)
        t = gauge.t
        q = gauge.q
        p = q[0,:]
        j = where(logical_and(t>t1-0.1,t<t2+0.1))[0]
        tt = t[j]
        pp = p[j]
        
        pfcn = interp1d(tt,pp)
        punif = pfcn(tunif)
        perr = abs(punif - pfine).max()
    
        cpu_times.append(cpu_time)
        perrs.append(perr)
    
    cpu_times = array(cpu_times)
    cpu_mean = mean(cpu_times)
    perrs = array(perrs)
    perrs_mean = mean(perrs)
    
    f.write('Case %s, CPU time mean = %s\n' % (case,cpu_mean))
    f.write('     CPU times: %s \n' % cpu_times)
    f.write('Case %s, error mean = %s\n' % (case,perrs_mean))
    f.write('     errors: %s \n' % perrs)


# file to collect statistics:
f = open('timings_errors.txt','w')
    
if 1:
    # adjont-error tests, with tolerance for each:
    cases = [('adjoint-error', 0.02), 
             ('adjoint-error', 0.01), 
             ('adjoint-error', 0.005), 
             ('adjoint-error', 0.0025)]
    for case in cases:
        rundata = setrun_cases.setrun()
        clawdata = rundata.clawdata 
        clawdata.num_cells[0] = 50
        clawdata.num_cells[1] = 40
        amrdata = rundata.amrdata
        amrdata.amr_levels_max = 6
        adjointdata = rundata.adjointdata
        adjointdata.use_adjoint = True
        amrdata.flag_richardson = True
        amrdata.flag_richardson_tol = case[1]
        amrdata.flag2refine = False
        if adjointdata.use_adjoint:
            # need an additional aux variable for inner product:
            rundata.amrdata.aux_type.append('center')
            rundata.clawdata.num_aux = len(rundata.amrdata.aux_type)
            adjointdata.innerprod_index = len(rundata.amrdata.aux_type)
        rundata.write()
        run_test(case)

if 1:
    # forward-error tests, with tolerance for each:
    cases = [('forward-error', 0.02*0.015), 
             ('forward-error', 0.01*0.015), 
             ('forward-error', 0.005*0.015), 
             ('forward-error', 0.0025*0.015)]
    for case in cases:
        rundata = setrun_cases.setrun()
        clawdata = rundata.clawdata 
        clawdata.num_cells[0] = 50
        clawdata.num_cells[1] = 40
        amrdata = rundata.amrdata
        amrdata.amr_levels_max = 6
        adjointdata = rundata.adjointdata
        adjointdata.use_adjoint = False
        amrdata.flag_richardson = True
        amrdata.flag_richardson_tol = case[1]
        amrdata.flag2refine = False
        if adjointdata.use_adjoint:
            # need an additional aux variable for inner product:
            rundata.amrdata.aux_type.append('center')
            rundata.clawdata.num_aux = len(rundata.amrdata.aux_type)
            adjointdata.innerprod_index = len(rundata.amrdata.aux_type)
        rundata.write()
        run_test(case)

        
if 1:
    # uniform grid tests, with (my,mx) for each:
    cases = [(1200,900), (800,600), (400,300)]
    #cases = [(100,80)]
    for case in cases:
        rundata = setrun_cases.setrun()
        clawdata = rundata.clawdata 
        clawdata.num_cells[0] = case[0]
        clawdata.num_cells[1] = case[1]
        clawdata.dt_initial = 0.005
        amrdata = rundata.amrdata
        amrdata.amr_levels_max = 1
        adjointdata = rundata.adjointdata
        adjointdata.use_adjoint = False
        amrdata.flag_richardson = False
        amrdata.flag_richardson_tol = -1.
        amrdata.flag2refine = False
        if adjointdata.use_adjoint:
            # need an additional aux variable for inner product:
            rundata.amrdata.aux_type.append('center')
            rundata.clawdata.num_aux = len(rundata.amrdata.aux_type)
            adjointdata.innerprod_index = len(rundata.amrdata.aux_type)
        rundata.write()
        run_test(case)

        if 0:
            cpu = []
            for k in range(5):
                runclaw.runclaw('xamr',outdir=outdir)
                timings = open('%s/timing.txt' % outdir).readlines()
                for line in timings:
                    if 'Total time:' in line:
                        tokens = line.split()
                        cpu.append(float(tokens[-1]))
            cpu = array(cpu)
            cpu_mean = mean(cpu)
            print('CPU times: ',cpu,' mean = ',cpu_mean)
            f.write('Case %s, CPU times: %s, mean = %s\n' % (case,cpu,cpu_mean))

f.close()
