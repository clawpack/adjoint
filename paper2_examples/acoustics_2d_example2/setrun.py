""" 
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.
    
"""

import os
import numpy as np


# This version is set up for adjoint flagging
#-----------------------------------------------



#------------------------------
def setrun(claw_pkg='amrclaw'):
#------------------------------

    """ 
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "amrclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData 
    
    """ 

    from clawpack.clawutil import data
    
 
    assert claw_pkg.lower() == 'amrclaw',  "Expected claw_pkg = 'amrclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)

    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------

    probdata = rundata.new_UserData(name='probdata',fname='setprob.data')
    probdata.add_param('p1',    2.,  'density on left')
    probdata.add_param('c1',    2.,  'sound speed on left')
    probdata.add_param('p2',    2.,  'density on right')
    probdata.add_param('c2',    1.,  'sound speed on right')
    
    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amrclaw.data for AMR)
    #------------------------------------------------------------------

    clawdata = rundata.clawdata  # initialized when rundata instantiated


    # Set single grid parameters first.
    # See below for AMR parameters.


    # ---------------
    # Spatial domain:
    # ---------------

    # Number of space dimensions:
    clawdata.num_dim = num_dim
    
    # Lower and upper edge of computational domain:
    clawdata.lower[0] = -8.000000e+00          # xlower
    clawdata.upper[0] = 8.000000e+00          # xupper
    clawdata.lower[1] = -1.000000e+00          # ylower
    clawdata.upper[1] = 11.000000e+00          # yupper
    
    # Number of grid cells:
    clawdata.num_cells[0] = 50 #1600 #50      # mx
    clawdata.num_cells[1] = 40 #1200 #50      # my
    

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    rundata.clawdata.num_aux = 2   
    # Note: as required for original problem - modified below for adjoint
    
    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 0
    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.000000
    

    # Restart from checkpoint file of a previous run?
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False               # True to restart from prior results
    clawdata.restart_file = 'fort.chk00006'  # File to use for restart data
    
    
    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
 
    clawdata.output_style = 2
 
    if clawdata.output_style==1:
        # Output ntimes frames at equally spaced times up to tfinal:
        # Can specify num_output_times = 0 for no output
        clawdata.num_output_times = 44
        clawdata.tfinal = 22.0
        clawdata.output_t0 = True  # output at initial (or restart) time?
        
    elif clawdata.output_style == 2:
        # Specify a list or numpy array of output times:
        # Include t0 if you want output at the initial time.
        clawdata.output_times =  [0., 2.5, 6., 15., 21., 22.]
 
    elif clawdata.output_style == 3:
        # Output every step_interval timesteps over total_steps timesteps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 10
        clawdata.output_t0 = True  # output at initial (or restart) time?
        

    clawdata.output_format = 'binary'       # 'ascii', 'binary', 'netcdf'

    clawdata.output_q_components = 'all'   # could be list such as [True,True]
    clawdata.output_aux_components = 'all'  # could be list
    clawdata.output_aux_onlyonce = False    # output aux arrays only at t0
    

    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:  
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 0
    
    

    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==True:  variable time steps used based on cfl_desired,
    # if dt_variable==False: fixed time steps dt = dt_initial always used.
    clawdata.dt_variable = True
    
    # Initial time step for variable dt.  
    # (If dt_variable==0 then dt=dt_initial for all steps)
    clawdata.dt_initial = 0.13
    
    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1.000000e+99
    
    # Desired Courant number if variable dt used 
    clawdata.cfl_desired = 0.900000
    # max Courant number to allow without retaking step with a smaller dt:
    clawdata.cfl_max = 1.000000
    
    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 50000


    # ------------------
    # Method to be used:
    # ------------------

    # Order of accuracy:  1 => Godunov,  2 => Lax-Wendroff plus limiters
    clawdata.order = 2
    
    # Use dimensional splitting? (not yet available for AMR)
    clawdata.dimensional_split = 'unsplit'
    
    # For unsplit method, transverse_waves can be 
    #  0 or 'none'      ==> donor cell (only normal solver used)
    #  1 or 'increment' ==> corner transport of waves
    #  2 or 'all'       ==> corner transport of 2nd order corrections too
    clawdata.transverse_waves = 2
    
    
    # Number of waves in the Riemann solution:
    clawdata.num_waves = 2
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'vanleer'  ==> van Leer
    #   4 or 'mc'       ==> MC limiter
    clawdata.limiter = ['vanleer','vanleer']
    
    clawdata.use_fwaves = False    # True ==> use f-wave version of algorithms
    
    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 0
    
    
    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2
    
    # Choice of BCs at xlower and xupper:
    #   0 or 'user'     => user specified (must modify bcNamr.f to use this option)
    #   1 or 'extrap'   => extrapolation (non-reflecting outflow)
    #   2 or 'periodic' => periodic (must specify this at both boundaries)
    #   3 or 'wall'     => solid wall for systems where q(2) is normal velocity
    
    clawdata.bc_lower[0] = 'wall'   # at xlower
    clawdata.bc_upper[0] = 'wall'   # at xupper

    clawdata.bc_lower[1] = 'extrap'   # at ylower
    clawdata.bc_upper[1] = 'wall'   # at yupper
                         

    # ---------------
    # Gauges:
    # ---------------
    rundata.gaugedata.gauges = []
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]
    rundata.gaugedata.gauges.append([0, 1.0, 5.5, 0., 1e9])

    # --------------
    # Checkpointing:
    # --------------

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 1

    if clawdata.checkpt_style == 0:
        # Do not checkpoint at all
        pass

    elif clawdata.checkpt_style == 1:
        # Checkpoint only at tfinal.
        pass

    elif clawdata.checkpt_style == 2:
        # Specify a list of checkpoint times.  
        clawdata.checkpt_times = [0.1,0.15]

    elif clawdata.checkpt_style == 3:
        # Checkpoint every checkpt_interval timesteps (on Level 1)
        # and at the final time.
        clawdata.checkpt_interval = 5

    

    # ---------------
    # AMR parameters:
    # ---------------

    amrdata = rundata.amrdata

    # max number of refinement levels:
    amrdata.amr_levels_max = 6

    # List of refinement ratios at each level (length at least amr_level_max-1)
    amrdata.refinement_ratios_x = [2,2,2,2,2,2,2,2,2]
    amrdata.refinement_ratios_y = [2,2,2,2,2,2,2,2,2]
    amrdata.refinement_ratios_t = [2,2,2,2,2,2,2,2,2]


    # Specify type of each aux variable in clawdata.auxtype.
    # This must be a list of length num_aux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).
    
    rundata.amrdata.aux_type = ['center','center']
    # Note: as required for original problem - modified below for adjoint
    
    # set tolerances for flagging in adjoint section below
    
    
    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 2       

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.7

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0      


    # ---------------
    # Regions:
    # ---------------
    rundata.regiondata.regions = []
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]

    #------------------------------------------------------------------
    # Adjoint specific data:
    #------------------------------------------------------------------
    # Also need to set flagging method and appropriate tolerances above

    flag_method = 'forward-error'

    assert flag_method in ['forward-diff','forward-error',\
           'adjoint-mag','adjoint-error'], '*** Unsupported flag_method'

    adjointdata = rundata.adjointdata
    adjointdata.use_adjoint = (flag_method in ['adjoint-mag','adjoint-error'])

    # Flag for refinement based on Richardson error estimater:
    amrdata.flag_richardson = (flag_method in ['adjoint-error','forward-error'])
    amrdata.flag_richardson_tol = 0.0025 #0.00005 # suggested if using adjoint-error flag

    # Flag for refinement using routine flag2refine:
    amrdata.flag2refine = (flag_method in ['adjoint-mag','forward-diff'])
    amrdata.flag2refine_tol = 0.001 # suggested if using adjoint-mag flag
    #amrdata.flag2refine_tol =  0.05 # suggested if using forward-diff

    # location of adjoint solution, must first be created:
    adjointdata.adjoint_outdir = os.path.abspath('adjoint/_output')

    # time period of interest:
    adjointdata.t1 = 20.5
    adjointdata.t2 = 21.5

    if adjointdata.use_adjoint:
        # need an additional aux variable for inner product:
        rundata.amrdata.aux_type.append('center')
        rundata.clawdata.num_aux = len(rundata.amrdata.aux_type)
        adjointdata.innerprod_index = len(rundata.amrdata.aux_type)
    
    
    #  ----- For developers -----
    # Toggle debugging print statements:
    amrdata.dprint = False      # print domain flags
    amrdata.eprint = False      # print err est flags
    amrdata.edebug = False      # even more err est flags
    amrdata.gprint = False      # grid bisection/clustering
    amrdata.nprint = False      # proper nesting output
    amrdata.pprint = False      # proj. of tagged points
    amrdata.rprint = False      # print regridding summary
    amrdata.sprint = False      # space/memory output
    amrdata.tprint = False      # time step reporting each level
    amrdata.uprint = False      # update/upbnd reporting
    
    return rundata

    # end of function setrun
    # ----------------------


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()
    
