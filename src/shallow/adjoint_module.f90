! ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
! ::::::     Module to define and work with adjoint type
! ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

module adjoint_module
    use amr_reload_module

    type adjointData_type

        integer lenmax, lendim, isize, lentot
        real(kind=8), allocatable, dimension(:) :: alloc

        real(kind=8) hxposs(maxlv), hyposs(maxlv),possk(maxlv)
        integer icheck(maxlv)

        ! for space management of alloc array
        integer lfree(lfdim,2),lenf

        real(kind=8) rnode(rsize, maxgr)
        integer node(nsize, maxgr), lstart(maxlv),newstl(maxlv), &
                listsp(maxlv)
        integer ibuff, mstart, ndfree, lfine, iorder, mxnest, &
                intratx(maxlv),intraty(maxlv), kratio(maxlv), &
                iregsz(maxlv),jregsz(maxlv), iregst(maxlv),jregst(maxlv), &
                iregend(maxlv),jregend(maxlv), numgrids(maxlv), kcheck, &
                nsteps, matlabu, iregridcount(maxlv)
        real(kind=8) time, tol, rvoll(maxlv),evol,rvol, &
                     cflmax, avenumgrids(maxlv)

        ! variable for conservation checking
        real(kind=8) tmass0

    end type adjointData_type

    type(adjointData_type), allocatable :: adjoints(:)
    integer :: totnum_adjoints, nvar, naux, num_adjoints, counter
    real(kind=8) :: trange_start, trange_final
    real(kind=8), allocatable :: adj_times(:)
    character(len=365), allocatable :: adj_files(:)

contains

    subroutine read_adjoint_data(adjointFolder)

        use amr_reload_module
        implicit none

        ! Function Arguments
        character(len=*), parameter :: adjointfile = 'adjoint.data'
        character(len=*), intent(in) :: adjointFolder
        logical :: fileExists
        integer :: iunit, k, r
        integer :: fileStatus = 0
        real(kind=8) :: finalT
        
        inquire(file=adjointfile, exist=fileExists)
        if (fileExists) then
            call amr2_reload(adjointFolder)
            iunit = 16
            call opendatafile(iunit,adjointfile)

            read(iunit,*) totnum_adjoints
            allocate(adj_times(totnum_adjoints))
            allocate(adj_files(totnum_adjoints))

            do 20 k = 1, totnum_adjoints
                read(iunit,*) adj_files(totnum_adjoints + 1 - k)
                read(iunit,*) adj_times(totnum_adjoints + 1 - k)
            20  continue
            close(iunit)

            finalT = adj_times(1)

            do 60 k = 1, totnum_adjoints
                ! Reverse times
                adj_times(k) = finalT - adj_times(k)
            60  continue

            ! Allocate space for the number of needed checkpoint files
            allocate(adjoints(totnum_adjoints))

            do 50 k = 1, totnum_adjoints
                ! Load checkpoint files
                call reload(adj_files(k),k)

                ! Reverse times
                adjoints(k)%time = adj_times(k)
            50 continue

        else
            print *, 'Error, adjoint.data file does not exist.'
        endif

    end subroutine read_adjoint_data

    subroutine set_time_window(t1, t2)

        implicit none

        ! Function Arguments
        real(kind=8), intent(in) :: t1, t2

        trange_final = t2
        trange_start = t1

    end subroutine set_time_window

    function calculate_max_innerproduct(t,x_c,y_c,q1,q2,q3,aux1) result(max_innerprod)

        use amr_reload_module
        implicit none

        real(kind=8), intent(in) :: t
        integer :: r
        real(kind=8) :: q_innerprod1, q_innerprod2, q_innerprod, max_innerprod
        double precision, allocatable :: q_interp(:)
        real(kind=8) :: x_c,y_c,q1,q2,q3
        real(kind=8) :: aux_interp1, aux_interp2, aux1, t_nm

        max_innerprod = 0.d0
        allocate(q_interp(nvar+1))

        aloop: do r=1, totnum_adjoints

        if (r .ne. 1) then
            t_nm = adjoints(r-1)%time
        else
            t_nm = 0.d0
        endif

        if (t < adjoints(r)%time .and. &
            (t +(trange_final - trange_start))>= t_nm) then

            call interp_adjoint(1, adjoints(r)%lfine, nvar, &
                naux, x_c,y_c,q_interp, r)
            aux_interp1 = q_interp(4) - q_interp(1)

            ! If q and q_adjoint aren't in the same wet/dry state 
            ! don't compute the inner product
            if(sign(aux1, aux_interp1) .ne. &
                sign(aux1, aux1)) then
                return
            endif

            if(aux_interp1 > 0.d0) then
                q_innerprod1 = abs( &
                  q1 * q_interp(1) &
                  + q2 * q_interp(2) &
                  + q3 * q_interp(3))
            else
                q_innerprod1 = abs( &
                  (q1+aux1) * q_interp(4) &
                  + q2 * q_interp(2) &
                  + q3 * q_interp(3))
            endif

            q_innerprod2 = 0.d0
            if (r .ne. 1) then
                call interp_adjoint(1, adjoints(r-1)%lfine, &
                    nvar, naux, x_c,y_c, q_interp, r-1)

                aux_interp2 = q_interp(4) - q_interp(1)

                ! If q and q_adjoint aren't in the same wet/dry state
                ! don't compute the inner product
                if(sign(aux1, aux_interp2) .ne. &
                    sign(aux1, aux1)) then
                    return
                endif

                if(aux_interp2 > 0.d0) then
                    q_innerprod2 = abs( &
                      q1 * q_interp(1) &
                      + q2 * q_interp(2) &
                      + q3 * q_interp(3))
                else
                    q_innerprod2 = abs( &
                      (q1+aux1) * q_interp(4) &
                      + q2 * q_interp(2) &
                      + q3 * q_interp(3))
                endif
            endif

            q_innerprod = max(q_innerprod1, q_innerprod2)
            if (q_innerprod > max_innerprod) then
                max_innerprod = q_innerprod
            endif
        endif

        enddo aloop

    end function calculate_max_innerproduct

end module adjoint_module
