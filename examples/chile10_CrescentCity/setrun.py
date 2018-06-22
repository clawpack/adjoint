"""
Module to set up run time parameters for Clawpack.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.

"""

from __future__ import absolute_import
from __future__ import print_function
import os
import numpy as np
#CC=os.environ['CC']

try:
    CLAW = os.environ['CLAW']
except:
    raise Exception("*** Must first set CLAW enviornment variable")

# Scratch directory for storing topo and dtopo files:
#scratch_dir = os.path.join(CLAW, 'geoclaw', 'scratch')



#-----------------------------------------------
# Set these parameters for adjoint flagging....

# location of output from computing adjoint:
adjoint_output = os.path.abspath('../adjoint_CrescentCity_26hrs/_output')
print('Will flag using adjoint solution from  %s' % adjoint_output)

# Time period of interest: doing a little test
t1 = 14.0*3600. 
t2 = 26.0*3600.

# tolerance for adjoint flagging:
adjoint_flag_tolerance = 7e-6
#-----------------------------------------------


#------------------------------
def setrun(claw_pkg='geoclaw'):
#------------------------------

    """
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "geoclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData

    """

    from clawpack.clawutil import data

    assert claw_pkg.lower() == 'geoclaw',  "Expected claw_pkg = 'geoclaw'"

    num_dim = 2
    rundata = data.ClawRunData(claw_pkg, num_dim)


    #------------------------------------------------------------------
    # Problem-specific parameters to be written to setprob.data:
    #------------------------------------------------------------------
    
    #probdata = rundata.new_UserData(name='probdata',fname='setprob.data')


    #------------------------------------------------------------------
    # GeoClaw specific parameters:
    #------------------------------------------------------------------
    rundata = setgeo(rundata)

    #------------------------------------------------------------------
    # Standard Clawpack parameters to be written to claw.data:
    #   (or to amr2ez.data for AMR)
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
    #clawdata.lower[0] = -240.0      # west longitude
    #clawdata.upper[0] = -100.0       # east longitude
    #clawdata.lower[1] = -41.0       # south latitude
    #clawdata.upper[1] = 65.0         # north latitude

    ### for chile, consider -48 as southern bdry and -66 as eastern
    ###          ,         -240, -66; -47, 65.  
    ###          , delta long = 87; delta lat = 56
    clawdata.lower[0] = -240.0      # west longitude
    clawdata.upper[0] = -66.0       # east longitude
    clawdata.lower[1] = -47.0       # south latitude
    clawdata.upper[1] = 65.0         # north latitude


    # Number of grid cells: Coarsest grid 2 degrees
    clawdata.num_cells[0] = 87
    clawdata.num_cells[1] = 56

    # ---------------
    # Size of system:
    # ---------------

    # Number of equations in the system:
    clawdata.num_eqn = 3

    # Number of auxiliary variables in the aux array (initialized in setaux)
    clawdata.num_aux = 3

    # Index of aux array corresponding to capacity function, if there is one:
    clawdata.capa_index = 2

    
    
    # -------------
    # Initial time:
    # -------------

    clawdata.t0 = 0.0


    # Restart from checkpoint file of a previous run?
    # If restarting, t0 above should be from original run, and the
    # restart_file 'fort.chkNNNNN' specified below should be in 
    # the OUTDIR indicated in Makefile.

    clawdata.restart = False              # True to restart from prior results
    clawdata.restart_file = 'fort.chk00096'  # File to use for restart data

    # -------------
    # Output times:
    #--------------

    # Specify at what times the results should be written to fort.q files.
    # Note that the time integration stops after the final output time.
    # The solution at initial time t0 is always written in addition.

    clawdata.output_style = 2
    #clawdata.output_style = 1

    if clawdata.output_style==1:
        # Output nout frames at equally spaced times up to tfinal:
        clawdata.num_output_times = 84
        clawdata.tfinal = 16*3600.
        clawdata.output_t0 = True  # output at initial (or restart) time?

    elif clawdata.output_style == 2:
        # Specify a list of output times.
        clawdata.output_times = np.linspace(1,26,51) * 3600.
        #clawdata.output_times = np.linspace(0,3,7) * 3600.

    elif clawdata.output_style == 3:
        # Output every iout timesteps with a total of ntot time steps:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 3
        clawdata.output_t0 = True
        

    #clawdata.output_format = 'ascii'      # 'ascii' or 'netcdf' 
    clawdata.output_format = 'binary'      # 'ascii' or 'netcdf' 

    clawdata.output_q_components = 'all'   # need all
    clawdata.output_aux_components = 'none'  # eta=h+B is in q
    clawdata.output_aux_onlyonce = False    # output aux arrays each frame



    # ---------------------------------------------------
    # Verbosity of messages to screen during integration:
    # ---------------------------------------------------

    # The current t, dt, and cfl will be printed every time step
    # at AMR levels <= verbosity.  Set verbosity = 0 for no printing.
    #   (E.g. verbosity == 2 means print only on levels 1 and 2.)
    clawdata.verbosity = 1



    # --------------
    # Time stepping:
    # --------------

    # if dt_variable==1: variable time steps used based on cfl_desired,
    # if dt_variable==0: fixed time steps dt = dt_initial will always be used.
    clawdata.dt_variable = True

    # Initial time step for variable dt.
    # If dt_variable==0 then dt=dt_initial for all steps:
    clawdata.dt_initial = 0.2

    # Max time step to be allowed if variable dt used:
    clawdata.dt_max = 1e+99

    # Desired Courant number if variable dt used, and max to allow without
    # retaking step with a smaller dt:
    clawdata.cfl_desired = 0.75
    clawdata.cfl_max = 1.0

    # Maximum number of time steps to allow between output times:
    clawdata.steps_max = 5000




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
    clawdata.num_waves = 3
    
    # List of limiters to use for each wave family:  
    # Required:  len(limiter) == num_waves
    # Some options:
    #   0 or 'none'     ==> no limiter (Lax-Wendroff)
    #   1 or 'minmod'   ==> minmod
    #   2 or 'superbee' ==> superbee
    #   3 or 'mc'       ==> MC limiter
    #   4 or 'vanleer'  ==> van Leer
    clawdata.limiter = ['mc', 'mc', 'mc']

    clawdata.use_fwaves = True    # True ==> use f-wave version of algorithms
    
    # Source terms splitting:
    #   src_split == 0 or 'none'    ==> no source term (src routine never called)
    #   src_split == 1 or 'godunov' ==> Godunov (1st order) splitting used, 
    #   src_split == 2 or 'strang'  ==> Strang (2nd order) splitting used,  not recommended.
    clawdata.source_split = 'godunov'


    # --------------------
    # Boundary conditions:
    # --------------------

    # Number of ghost cells (usually 2)
    clawdata.num_ghost = 2

    # Choice of BCs at xlower and xupper:
    #   0 => user specified (must modify bcN.f to use this option)
    #   1 => extrapolation (non-reflecting outflow)
    #   2 => periodic (must specify this at both boundaries)
    #   3 => solid wall for systems where q(2) is normal velocity

    clawdata.bc_lower[0] = 'extrap'
    clawdata.bc_upper[0] = 'extrap'

    clawdata.bc_lower[1] = 'extrap'
    clawdata.bc_upper[1] = 'extrap'



    # --------------
    # Checkpointing:
    # --------------

    # Specify when checkpoint files should be created that can be
    # used to restart a computation.

    clawdata.checkpt_style = 0

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
    amrdata.amr_levels_max = 8

    # List of refinement ratios at each level (length at least mxnest-1)

    #1sec
    # 2 degree, 24', 4', 1', 12", 6", 1"  for 7 levels.
    #amrdata.refinement_ratios_x = [5, 6, 4, 5, 2, 6]
    #amrdata.refinement_ratios_y = [5, 6, 4, 5, 2, 6]
    #amrdata.refinement_ratios_t = [5, 6, 4, 5, 2, 6]


    #2sec
    # 2 degree, 24', 4', 1', 12", 6", 2"  for 7 levels.
    #amrdata.refinement_ratios_x = [5, 6, 4, 5, 2, 3]
    #amrdata.refinement_ratios_y = [5, 6, 4, 5, 2, 3]
    #amrdata.refinement_ratios_t = [5, 6, 4, 5, 2, 3]

    #1/3sec, trying one with 8 levels, including 6sec region
    # 2 degree, 24', 4', 1', 12", 6", 1", 1/3" for 8 levels.
    # level 5 is still 12". level 6 is 6", level 7 is 1 sec, and level 8 is 1/3
    amrdata.refinement_ratios_x = [5, 6, 4, 5, 2, 6, 3]
    amrdata.refinement_ratios_y = [5, 6, 4, 5, 2, 6, 3]
    amrdata.refinement_ratios_t = [5, 6, 4, 5, 2, 6, 3]

    # Specify type of each aux variable in amrdata.auxtype.
    # This must be a list of length maux, each element of which is one of:
    #   'center',  'capacity', 'xleft', or 'yleft'  (see documentation).

    amrdata.aux_type = ['center','capacity','yleft']


    # Flag using refinement routine flag2refine rather than richardson error
    amrdata.flag_richardson = False    # use Richardson?
    amrdata.flag2refine = True

    # steps to take on each level L between regriddings of level L+1:
    amrdata.regrid_interval = 3

    # width of buffer zone around flagged points:
    # (typically the same as regrid_interval so waves don't escape):
    amrdata.regrid_buffer_width  = 2

    # clustering alg. cutoff for (# flagged pts) / (total # of cells refined)
    # (closer to 1.0 => more small grids may be needed to cover flagged cells)
    amrdata.clustering_cutoff = 0.700000

    # print info about each regridding up to this level:
    amrdata.verbosity_regrid = 0  

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
    
    # More AMR parameters can be set -- see the defaults in pyclaw/data.py

    # ---------------------------------------------------------------
    #1sec
    # 2 degree, 24', 4', 1', 12", 1" 6 levels.
    # --------------------------------------------------------------
    rundata.regiondata.regions = []
    # to specify regions of refinement append lines of the form
    #  [minlevel,maxlevel,t1,t2,x1,x2,y1,y2]

    # Ocean refinement from Chile, using adjoint, below is whole domain 
    rundata.regiondata.regions.append([1, 5, 0., 1e9, -240,-66,-47,65])
    #rundata.regiondata.regions.append([1, 4, 13.0*3600., 1e9, -160,-120,34,62])
    #rundata.regiondata.regions.append([1, 4, 10.5*3600., 1e9, -160,-110,18,34])

    # Chile source:
    # Note, we are using 1 minute around the source. It may not be necessary.
    ### domain,         -240, -66; -47, 65.  
    ### pink deformation has region:  -94.65, -67.9833; -46.294, -24.8641
    #rundata.regiondata.regions.append([4, 4, 0., 4.0*3600, -96.0,-68.0,-47.0,-24.0])
    # above region is from Loyce. Trying a smaller source region:
    rundata.regiondata.regions.append([4, 4, 0., 4.0*3600, -80.0,-68.0,-40.0,-20.0])

    #Port Orford   (lat: 42degrees, 44.3min, long: 124degrees, 29.9min)
    #Crescent City (lat: 41degrees, 44.7min, long: 124degrees, 11.1min)
    #Arena Cove    (lat: 38degrees, 54.9min, long: 123degrees, 42.7min)
    #San Luis      (lat: 35degrees, 10.1min, long: 120degrees, 45.2min)

    #Make a new bigger A grid:
    #rundata.regiondata.regions.append([1, 4, 13.0*3600., 1e9, -129,-123,38,46])

    #Diego's A grid becomes the B (12sec) grid:
    #rundata.regiondata.regions.append([4, 4, 14.0*3600., 1e9, -126.995,-123.535,40.515,44.495])
    #rundata.regiondata.regions.append([1, 5, 14.0*3600., 1e9, -126.995,-123.535,40.515,44.495])

    #Diego's B grid becomes a 6sec grid:
    rundata.regiondata.regions.append([1, 6, 14.5*3600., 1e9, -124.6,-124.05,41.5017,41.9983])

    #For the 1sec and 2sec runs, match Diego C grid as below for 7,7
    #For the UW topo, use this one for the 1sec as well when doing 1/3
    #Too much land
    #rundata.regiondata.regions.append([7, 7, 14.5*3600., 1e9, -124.2345, -124.1434,41.7168,41.7829])

    #For the 1/3 run, make region 6 match the 1/3 data with 1sec computation
    #Use this even for UW 1/3 run
    rundata.regiondata.regions.append([1, 7, 14.5*3600., 1e9, -124.2345, -124.1595,41.7168,41.76948])

    #Trying a 1/3 grid close in  (our D grid)
    rundata.regiondata.regions.append([1, 8, 14.5*3600., 1e9, -124.202, -124.180,41.733,41.752])

    # ---------------
    # Gauges:
    # ---------------
    rundata.gaugedata.gauges = []
    # for gauges append lines of the form  [gaugeno, x, y, t1, t2]


    #from Diego file

    rundata.gaugedata.gauges.append([2, -124.18397, 41.74512, 14.5*3600., 1.e10])

    #------------------------------------------------------------------
    # Adjoint specific data:
    #------------------------------------------------------------------
    # Do this last since it resets some parameters such as num_aux
    # as needed for adjoint flagging.
    rundata = setadjoint(rundata)



    return rundata
    # end of function setrun
    # ----------------------


#-------------------
def setgeo(rundata):
#-------------------
    """
    Set GeoClaw specific runtime parameters.
    For documentation see ....
    """

    try:
        geo_data = rundata.geo_data
    except:
        print("*** Error, this rundata has no geo_data attribute")
        raise AttributeError("Missing geo_data attribute")
       
    # == Physics ==
    geo_data.gravity = 9.81
    geo_data.coordinate_system = 2
    geo_data.earth_radius = 6367.5e3

    # == Forcing Options
    geo_data.coriolis_forcing = False

    # == Algorithm and Initial Conditions ==
    geo_data.sea_level = 0 # -1.5
    geo_data.dry_tolerance = 1.e-3
    geo_data.friction_forcing = True
    geo_data.manning_coefficient =.025
    geo_data.friction_depth = 1e6

    # Refinement settings
    refinement_data = rundata.refinement_data
    refinement_data.variable_dt_refinement_ratios = True
    refinement_data.wave_tolerance = 0.002
    refinement_data.deep_depth = 1e2
    #refinement_data.max_level_deep = 3 (changing to 4)
    refinement_data.max_level_deep = 4

    # == settopo.data values ==
    topo_data = rundata.topo_data
    # for topography, append lines of the form
    #    [topotype, minlevel, maxlevel, t1, t2, fname]

    #topo_dir = '../../topo_for_runs/'  ## for new set of topo files
    #topo_dir = '../../topo/PacificDEMs/'
    #topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
    #    topo_dir+'etopo1_-180_-60_-65_65_4min.tt3'])
    #topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
    #    topo_dir+'etopo1_-240_-180_-65_65_4min.tt3'])

    # The 1 minute file files.
    #topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
    #    topo_dir+'etopo1_-240_-180_-41_65_1min.tt3'])
    #topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
    #    topo_dir+'etopo1_-180_-100_-41_65_1min.tt3'])
    ### domain,         -240, -66; -47, 65.  
    #
    #Need the new 1 minute files below.
    #topo_dir = '../../topo/etopo/'  ## for new set of topo files
    topo_dir = '../../topo_for_runs/'  ## for new set of topo files
    topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
        topo_dir+'etopo1_-240_-180_-47_65_1min.tt3'])
    topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
        topo_dir+'etopo1_-180_-66_-47_65_1min.tt3'])

    ## Around Crescent City
    ### Diegos 1sec topo, was pierless
    ### This is used for the 1sec and 2 sec runs for Japan2011
    ### and Samoa2009 1 and 2 sec run. Use here for Chile 1sec run
    #topo_dir = '../../topo/PMEL/'
    #topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
    #    topo_dir+'cresc1sec.asc'])

    #These are the UW topo files for Crescent City
    #topo_dir = CC + '/topo/'
    topo_data.topofiles.append([3, 1, 1, 0., 1.e10, \
       topo_dir+'cc-1_3sec-c_pierless.asc'])
    topo_data.topofiles.append([-3, 1, 1, 0., 1.e10, \
       topo_dir+'cc-1sec-c.asc'])


    # == setdtopo.data values ==
    dtopo_data = rundata.dtopo_data
    # for moving topography, append lines of the form :   (<= 1 allowed for now!)
    #   [topotype, minlevel,maxlevel,fname]
    ### pink deformation has region:  -94.65, -67.9833; -46.294, -24.8641
    ### This is about 27 degees by 25 degrees deltas. at one min 27*60 by 25*60
    dtopo_path = '../../dtopo/2010Chile_deformation_most.asc'
    dtopo_data.dtopofiles.append([3,1,1,dtopo_path])
    dtopo_data.dt_max_dtopo = 0.2


    # == setqinit.data values ==
    rundata.qinit_data.qinit_type = 0
    rundata.qinit_data.qinitfiles = []
    # for qinit perturbations, append lines of the form: (<= 1 allowed for now!)
    #   [minlev, maxlev, fname]

    # == setfixedgrids.data values ==
    fixed_grids = rundata.fixed_grid_data
    # for fixed grids append lines of the form
    # [t1,t2,noutput,x1,x2,y1,y2,xpoints,ypoints,\
    #  ioutarrivaltimes,ioutsurfacemax]

    return rundata
    # end of function setgeo
    # ----------------------


#-------------------
def setadjoint(rundata):
#-------------------

    """
    Set parameters used for adjoint flagging.
    Also reads in all of the checkpointed Adjoint files.
    """
    
    import glob

    # Set these parameters at top of this file:
    # adjoint_flag_tolerance, t1, t2, adjoint_output
    # Then you don't need to modify this function...

    rundata.amrdata.flag2refine = True  # for adjoint flagging
    rundata.amrdata.flag2refine_tol = adjoint_flag_tolerance

    rundata.clawdata.num_aux = 4   # 4 required for adjoint flagging
    rundata.amrdata.aux_type = ['center','capacity','yleft','center']

    adjointdata = rundata.new_UserData(name='adjointdata',fname='adjoint.data')
    adjointdata.add_param('adjoint_output',adjoint_output,'adjoint_output')
    adjointdata.add_param('t1',t1,'t1, start time of interest')
    adjointdata.add_param('t2',t2,'t2, final time of interest')

    files = glob.glob(os.path.join(adjoint_output,"fort.b*"))

    files.sort()

    if (len(files) == 0):
        print("No binary files found for adjoint output!")
    
    adjointdata.add_param('numadjoints', len(files), 
                       'Number of adjoint output files.')
    adjointdata.add_param('innerprod_index', 4, 
                       'Index for innerproduct data in aux array.')

    counter = 1
    for fname in files:
        f = open(fname)
        adjointdata.add_param('file' + str(counter), fname, \
            'Binary file' + str(counter))
        counter = counter + 1

    return rundata
    # end of function setadjoint
    # ----------------------


if __name__ == '__main__':
    # Set up run-time parameters and write all data files.
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()

    from clawpack.geoclaw import kmltools
    kmltools.make_input_data_kmls(rundata)
