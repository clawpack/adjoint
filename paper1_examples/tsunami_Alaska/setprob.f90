subroutine setprob()

    use geoclaw_module
    use topo_module
    use qinit_module
    use fixedgrids_module
    use refinement_module
    use adjoint_module, only: read_adjoint_data, set_time_window

    implicit none
    character(len=7) ::  adjointFolder

    !# Defining time window of interest
    real(kind=8) :: t1, t2
    t1 = 3.5*3600.
    t2 = 11*3600.

    ! # Setting up folder to read adjoint data from
    adjointFolder = 'adjoint'

    call set_geo()                             !# sets basic parameters g and coord system
    call set_refinement()                      !# sets refinement control parameters
    call read_dtopo_settings()                 !# specifies file with dtopo from earthquake
    call read_topo_settings()                  !# specifies topography (bathymetry) files
    call set_qinit()                           !# specifies file with dh if this used instead
    call set_fixed_grids()                     !# Fixed grid settings
    call set_time_window(t1, t2)               !# Set time window
    call read_adjoint_data(adjointFolder)      !# Reading adjoint data

end subroutine setprob
